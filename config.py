from utils.releases import get_ruwa_versions

# Dynamically fetch available Ruwa versions.
VERSIONS = get_ruwa_versions()

# Or use a fixed list of versions:
# VERSIONS = [
#     "0.3.4-alpha",
#     "0.3.3-alpha",
# ]
