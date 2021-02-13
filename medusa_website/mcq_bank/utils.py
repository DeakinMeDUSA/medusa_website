import fnmatch

from manifest_loader.loaders import LoaderABC


class CustomManifestReactLoader(LoaderABC):
    @staticmethod
    def get_single_match(manifest, key):
        search_dict = manifest
        if manifest.get("files") is not None:
            search_dict = manifest["files"]
        return search_dict.get(key, key)

    @staticmethod
    def get_multi_match(manifest, pattern):
        # search_dict = [manifest]
        # if manifest.get("files") is not None:
        #     search_dicts.append(manifest["files"])
        # if manifest.get("entrypoints") is not None:
        #     search_dicts.append({val: val for val in manifest["entrypoints"]})
        # # print(f"search_dicts = {search_dicts}")
        # matched_files = []
        # for search_dict in search_dicts:
        #     for matched_key in [file for file in search_dict.keys() if fnmatch.fnmatch(file, pattern)]:
        #         matched_files.append(search_dict.get(matched_key))
        # return list(set(matched_files))
        search_list = manifest.get("entrypoints", [])
        if len(search_list) == 0:
            raise RuntimeError("No entrypoints found in manifest file!")
        print(f"search_list = {search_list}")
        matched_files = [file for file in search_list if fnmatch.fnmatch(file, pattern)]
        print(f"pattern = {pattern} | matched_files = {matched_files}")

        return list(set(matched_files))
