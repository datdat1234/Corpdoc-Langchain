########################## LIBRARY ###############################

from unidecode import unidecode

##################################################################

hu_cau = [
    "Hư cấu kỳ ảo",
    "Khoa học viễn tưởng",
    "Phản địa đàng",
    "Hành động và Phiêu lưu",
    "Thần bí và Trinh thám",
    "Kinh dị",
    "Hài hước",
    "Giật gân",
    "Lịch sử hư cấu",
    "Tình cảm",
    "Văn học đương đại",
    "Chủ nghĩa hiện thực huyền ảo",
    "Tiểu thuyết hình ảnh",
    "Truyện ngắn",
    "Thanh niên",
    "Người lớn",
    "Trẻ em",
    "Tiểu thuyết dành cho phụ nữ",
]

phi_hu_cau = [
    "Tiểu sử",
    "Hồi ký và tự truyện",
    "Đồ ăn và thức uống hay sách nấu ăn",
    "Mỹ thuật và Tranh ảnh",
    "Văn học du lịch",
    "Tội phạm có thật",
    "Hài",
    "Tiểu luận",
    "Hướng dẫn",
    "Tâm linh",
    "Khoa học xã hội và nhân văn",
    "Khoa học và Công nghệ",
    "Sách giáo khoa",
    "Tự lực",
    "Lịch sử",
]


def getDocType(title: str):
    doc_types = [
        "ban-ghi-nho",
        "ban-thoa-thuan",
        "bao-cao",
        "bien-ban",
        "chuong-trinh",
        "cong-thu",
        "cong-van",
        "de-an",
        "du-an",
        "giay-gioi-thieu",
        "giay-moi",
        "giay-nghi-phep",
        "giay-uy-quyen",
        "hop-dong",
        "huong-dan",
        "ke-hoach",
        "nghi-quyet",
        "phieu-bao",
        "phieu-chuyen",
        "phieu-gui",
        "phuong-an",
        "quy-che",
        "quy-dinh",
        "quyet-dinh",
        "thong-bao",
        "thong-cao",
        "to-trinh",
    ]

    normalized_title = unidecode(title).lower().replace(" ", "-")

    for doc_type in doc_types:
        if doc_type in normalized_title:
            position_find = normalized_title.find(doc_type)
            if position_find == 0 or position_find == 1:
                return doc_type

    return None


def returnVBHCPath(type):
    if type == "ban-ghi-nho":
        return "Bản ghi nhớ"
    elif type == "ban-thoa-thuan":
        return "Bản thỏa thuận"
    elif type == "bao-cao":
        return "Báo cáo"
    elif type == "bien-ban":
        return "Biên bản"
    elif type == "chuong-trinh":
        return "Chương trình"
    elif type == "cong-thu":
        return "Công thư"
    elif type == "cong-van":
        return "Công văn"
    elif type == "de-an":
        return "Đề án"
    elif type == "du-an":
        return "Dự án"
    elif type == "giay-gioi-thieu":
        return "Giấy giới thiệu"
    elif type == "giay-moi":
        return "Giấy mời"
    elif type == "giay-nghi-phep":
        return "Giấy nghỉ phép"
    elif type == "giay-uy-quyen":
        return "Giấy ủy quyền"
    elif type == "hop-dong":
        return "Hợp đồng"
    elif type == "huong-dan":
        return "Hướng dẫn"
    elif type == "ke-hoach":
        return "Kế hoạch"
    elif type == "nghi-quyet":
        return "Nghị quyết"
    elif type == "phieu-bao":
        return "Phiếu báo"
    elif type == "phieu-chuyen":
        return "Phiếu chuyển"
    elif type == "phieu-gui":
        return "Phiếu gửi"
    elif type == "phuong-an":
        return "Phương án"
    elif type == "quy-che":
        return "Quy chế"
    elif type == "quy-dinh":
        return "Quy định"
    elif type == "quyet-dinh":
        return "Quyết định"
    elif type == "thong-bao":
        return "Thông báo"
    elif type == "thong-tu":
        return "Thông tư"
    elif type == "to-trinh":
        return "Tờ trình"
    else:
        return "Khác"


def setCriteriaPath(doc_type, type_path, criteria):
    if doc_type == "admin-doc":
        criteria[0] = type_path + "/" + criteria[0]
        return criteria
    if doc_type == "book":
        modified_criteria = []
        for criterion in criteria:
            if criterion in hu_cau:
                criterion = type_path + "Truyện, sách hư cấu/" + criterion
            else:
                criterion = type_path + "Sách phi hư cấu/" + criterion
            modified_criteria.append(criterion)
        return modified_criteria
