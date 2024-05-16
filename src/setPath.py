########################## LIBRARY ###############################

from unidecode import unidecode

##################################################################

#######################   FUNCTION   #############################

from src.dataLoader import queryData

##################################################################

########################## VARIABLE ##############################

from src.envLoader import (
    vbhc_query_level1,
    vbhc_query_level2,
    book_query_hc,
    book_query_phc,
)

##################################################################


def convert_string_to_list(string):
    lines = string.split("\n")
    unique_lines = list(set(lines))
    unique_lines.remove("")  # Remove empty lines if present
    return unique_lines


def remove_first_character_and_trim(arr):
    return [s[1:].strip() for s in arr]


def create_key_value_pairs(arr):
    return [{s: unidecode(s).lower().replace(" ", "-")} for s in arr]


hu_cau = remove_first_character_and_trim(
    convert_string_to_list(queryData(book_query_hc))
)

phi_hu_cau = remove_first_character_and_trim(
    convert_string_to_list(queryData(book_query_phc))
)

vbhc_types = remove_first_character_and_trim(
    convert_string_to_list(queryData(vbhc_query_level2))
)

doc_types = create_key_value_pairs(vbhc_types)

def getDocType(title: str):
    normalized_title = unidecode(title).lower().replace(" ", "-")

    doc_type_tmp = None
    doc_min_position = 1000000

    for doc_type in doc_types:
        for value in doc_type.values():
            if value in normalized_title:
                position_find = normalized_title.find(value)
                if position_find < doc_min_position:
                    doc_min_position = position_find
                    doc_type_tmp = value

    return doc_type_tmp


def returnVBHCPath(type):
    for item in doc_types:
        for key, value in item.items():
            if value == type:
                return key
    return "Khác"


def setCriteriaPath(doc_type, type_path, criteria, level2_type):
    modified_criteria = []
    if doc_type == "admin-doc":
        for criterion in criteria:
            modified_criteria.append(type_path + criterion + "/" + level2_type)
        return modified_criteria
    if doc_type == "book":
        for criterion in criteria:
            if criterion in hu_cau:
                modified_criteria.append(type_path + "Hư cấu/" + criterion)
            if criterion in phi_hu_cau:
                modified_criteria.append(type_path + "Phi hư cấu/" + criterion)
        return modified_criteria
