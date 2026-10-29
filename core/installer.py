import logging
import platform
import shutil
import subprocess
from pathlib import Path, PurePath

from utils.exceptions import UnsupportedDistributionError
from utils.packages import DISTRO_PACKAGES

logger = logging.getLogger("RuwaInstaller")


class RuwaInstaller:
    __project_path = "/tmp/ruwa"
    __build_path = "/tmp/ruwa/build"
    app_default_path = ""
    options = {}
    version = ""

    def __init__(self, options: dict, version: str, path: PurePath | str):
        RuwaInstaller.app_default_path = path
        RuwaInstaller.options = options
        RuwaInstaller.version = version

        logger.info("Initializing Ruwa installer")
        logger.info("Installation path: %s", path)
        logger.info("Options: %s", options)
        logger.info("Version: %s", version)

    @staticmethod
    def get_distro_and_like() -> tuple[str, list[str]]:
        os_info = platform.freedesktop_os_release()
        distro = os_info.get("ID", "").lower()
        like = os_info.get("ID_LIKE", "").lower().split()

        logger.info("Distro: %s", distro)
        return distro, like

    @staticmethod
    def get_dependencies_for_distro(distro: str, like: list[str]) -> list[str] | None:
        if distro == "arch" or "arch" in like:
            return DISTRO_PACKAGES["arch"]

        if distro == "debian" or "debian" in like:
            return DISTRO_PACKAGES["debian"]

        if distro == "fedora" or "fedora" in like:
            return DISTRO_PACKAGES["fedora"]

        logger.warning("Unsupported distro: %s", distro)
        return None

    @staticmethod
    def get_package_install_command(distro: str, like: list[str]):
        if distro == "arch" or "arch" in like:
            return ["pacman", "-S"]

        elif distro in ("debian", "ubuntu", "linuxmint") or "debian" in like:
            return ["apt", "install"]

        elif distro in ("fedora", "rhel", "rocky", "almalinux") or "fedora" in like:
            return ["dnf", "install"]

        else:
            logger.warning("Unsupported distro: %s", distro)

    @staticmethod
    def __get_package_check_command(distro: str, like: list[str]) -> list[str] | None:
        if distro == "arch" or "arch" in like:
            return ["pacman", "-Q"]

        elif distro in ("debian", "ubuntu", "linuxmint") or "debian" in like:
            return ["dpkg", "-s"]

        elif distro in ("fedora", "rhel", "rocky", "almalinux") or "fedora" in like:
            return ["rpm", "-q"]

        else:
            logger.warning("Unsupported distro: %s", distro)

    @staticmethod
    def check_packages() -> list[str]:
        distro, like = RuwaInstaller.get_distro_and_like()
        packages = RuwaInstaller.get_dependencies_for_distro(distro, like)
        package_check_command = RuwaInstaller.__get_package_check_command(distro, like)

        if package_check_command is None or packages is None:
            raise UnsupportedDistributionError(
                f"Unsupported Linux distribution: {distro or 'unknown'}"
            )

        missing = []
        for package in packages:
            result = subprocess.run(
                package_check_command + [package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            if result.returncode != 0:
                logger.warning("Package is not installed: %s", package)
                missing.append(package)
            else:
                logger.info("Package is installed: %s", package)
        if missing:
            logger.error("Missing packages: %s", ", ".join(missing))

        return missing

    @staticmethod
    def download_ruwa() -> str | None:
        path = RuwaInstaller.__project_path

        logger.info("Starting Ruwa download...")
        logger.info("Repository: https://github.com/LuskusDeus/Ruwa.git")
        logger.info("Version/branch: %s", RuwaInstaller.version)

        if Path(path).exists():
            shutil.rmtree(path)

        result = subprocess.run(
            [
                "git",
                "clone",
                "-b",
                RuwaInstaller.version,
                "https://github.com/LuskusDeus/Ruwa.git",
                path,
            ],
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            error = result.stderr.strip()
            logger.error("git clone failed: %s", error)
            return error
        logger.info("Ruwa source downloaded successfully.")
        return None

    @staticmethod
    def __fix_lasso_shader_check():
        file_path = (
            Path(RuwaInstaller.__project_path)
            / "src/shared/rendering/ShaderDirectoryResolver.cpp"
        )
        logger.info("Applying patch fix lasso shader: %s", file_path)

        old = '        QStringLiteral("lasso_mask.comp.glsl"),'
        new = '//        QStringLiteral("lasso_mask.comp.glsl"),'

        with open(
            file_path,
            "r+",
            encoding="utf-8",
        ) as f:
            content = f.read()
            if old not in content:
                logger.warning("Lasso shader check line not found: %s", file_path)
                return
            content = content.replace(old, new, 1)
            f.seek(0)
            f.write(content)
            f.truncate()

    @staticmethod
    def __apply_patches():
        try:
            RuwaInstaller.__fix_lasso_shader_check()
            file_path = (
                Path(RuwaInstaller.__project_path)
                / "plugins/standard/distort/src/effects/Pinch.c"
            )
            logger.info("Applying patch: %s", file_path)

            with open(
                file_path,
                "r+",
                encoding="utf-8",
            ) as f:
                content = f.read()

                if "#include <math.h>" not in content:
                    f.seek(0, 0)
                    f.write("#include <math.h>\n")
                    f.write(content)

            logger.info("Patch applied successfully.")
            return None

        except OSError as e:
            logger.error("File operation failed: %s", e)
            return str(e)

    @staticmethod
    def configure() -> str | None:
        RuwaInstaller.__apply_patches()
        logger.info("Starting CMake configuration...")
        dbuild_testing_val = RuwaInstaller.options.pop("-DBUILD_TESTING", None)

        cmake_args = [
            "cmake",
            "-S",
            RuwaInstaller.__project_path,
            "-B",
            RuwaInstaller.__build_path,
            "-G",
            "Ninja",
            "-DCMAKE_BUILD_TYPE=Release",
        ]

        if dbuild_testing_val is not None:
            logger.info("DBUILD_TESTING - %s", dbuild_testing_val)
            cmake_args.append(f"-DBUILD_TESTING={dbuild_testing_val}")

        result = subprocess.run(cmake_args, capture_output=True, text=True)

        if result.returncode != 0:
            error = result.stderr.strip()
            logger.error("CMake configuration failed:\n%s", error)
            return error

        logger.info("CMake configuration completed successfully.")
        return None

    @staticmethod
    def build() -> str | None:
        logger.info("Starting Ruwa build...")

        result = subprocess.run(
            ["cmake", "--build", RuwaInstaller.__build_path, "-j"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if result.returncode != 0:
            error = result.stdout.strip()
            logger.error("Build failed:\n%s", error)
            return error

        logger.info("Ruwa build completed successfully.")
        return None

    @staticmethod
    def install():
        destination_app = Path(RuwaInstaller.app_default_path).expanduser()
        destination_app.mkdir(parents=True, exist_ok=True)

        logger.info("Starting installation...")
        logger.info("Installation directory: %s", destination_app)

        build_path = Path(RuwaInstaller.__build_path)
        resources = [
            build_path / "effects",
            build_path / "plugins",
            build_path / "Ruwa",
            build_path / "shaders",
            build_path / "RuwaPigmentLutGenerator",
            build_path / "out-x86_64-Release" / "lib",
        ]
        logger.info("Checking build resources...")
        try:
            for resource in resources:
                if not resource.exists():
                    error = f"Required resource not found: {resource}"
                    logger.error(error)
                    return error

                logger.info("Found: %s", resource)

                destination = destination_app / resource.name
                if resource.is_dir():
                    shutil.copytree(
                        resource,
                        destination,
                        dirs_exist_ok=True,
                    )
                else:
                    shutil.copy2(resource, destination)

        except OSError as e:
            logger.exception("Installation failed")
            return str(e)

        logger.info("Installation completed successfully.")
        return None

    @staticmethod
    def create_shortcut():
        logger.info("Creating desktop entry...")

        destination = Path("~/.local/share/applications").expanduser()
        destination_app = Path(RuwaInstaller.app_default_path).expanduser()
        destination_app.mkdir(parents=True, exist_ok=True)

        env_string = " ".join(
            f"{key}={value}"
            for key, value in RuwaInstaller.options.items()
            if key != "add_shortcut"
        )

        desktop_file = destination / "ruwa.desktop"
        CONTENT = f"""[Desktop Entry]
Type=Application
Name=Ruwa
Exec=env LD_LIBRARY_PATH={destination_app / "lib"} {env_string} {destination_app}/Ruwa %U
Icon=ruwa
Terminal=false
Categories=Graphics;
MimeType=image/jpeg;image/png;image/webp;image/svg+xml;
"""
        with open(desktop_file, "w", encoding="utf-8") as f:
            f.write(CONTENT)

        subprocess.run(["update-desktop-database", str(destination)], check=True)


if __name__ == "__main__":
    installer = RuwaInstaller(
        options={"QT_QPA_PLATFORMTHEME": "xdgdesktopportal", "QT_QPA_PLATFORM": "xcb"},
        path="~/.local/bin/ruwa-test",
    )
    installer.check_packages()
    installer.download_ruwa()
    installer.configure()
    installer.build()
    installer.install()
    installer.create_shortcut()
