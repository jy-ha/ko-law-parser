from core import parse_law, delete_deleted_laws, save_json


if __name__ == "__main__":
    law_dict = parse_law("law/국세기본법.txt")
    law_dict = delete_deleted_laws(law_dict)
    save_json(law_dict, "law/국세기본법.json")