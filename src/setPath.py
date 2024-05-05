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
        "chi-thi",
        "cong-dien",
        "don",
        "giay-de-nghi",
        "cong-bo",
        "dieu-le",
        "thoa-uoc",
        "giay-xac-nhan",
        "xac-nhan",
        "giay-dang-ky",
        "giay-chung-nhan",
        "giay-bien-nhan",
        "thu",
        "noi-quy",
        "phieu-lay-y-kien",
        "giay-phep",
        "chung-chi",
        "to-khai",
        "ban-cam-ket",
        "giay-cam-ket",
        "cam-ket",
    ]

    normalized_title = unidecode(title).lower().replace(" ", "-")

    doc_type_tmp = None
    doc_min_position = 1000000

    for doc_type in doc_types:
        if doc_type in normalized_title:
            position_find = normalized_title.find(doc_type)
            if position_find < doc_min_position:
                doc_min_position = position_find
                doc_type_tmp = doc_type

    return doc_type_tmp


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
    elif type == "thong-cao":
        return "Thông cáo"
    elif type == "to-trinh":
        return "Tờ trình"
    elif type == "chi-thi":
        return "Chỉ thị"
    elif type == "cong-dien":
        return "Công điện"
    elif type == "don":
        return "Đơn"
    elif type == "giay-de-nghi":
        return "Giấy đề nghị"
    elif type == "cong-bo":
        return "Công bố"
    elif type == "dieu-le":
        return "Điều lệ"
    elif type == "thoa-uoc":
        return "Thỏa ước"
    elif type == "giay-xac-nhan" or type == "xac-nhan":
        return "Giấy xác nhận"
    elif type == "giay-dang-ky":
        return "Giấy đăng ký"
    elif type == "giay-chung-nhan":
        return "Giấy chứng nhận"
    elif type == "giay-bien-nhan":
        return "Giấy biên nhận"
    elif type == "thu":
        return "Thư"
    elif type == "noi-quy":
        return "Nội quy"
    elif type == "phieu-lay-y-kien":
        return "Phiếu lấy ý kiến"
    elif type == "giay-phep":
        return "Giấy phép"
    elif type == "chung-chi":
        return "Chứng chỉ"
    elif type == "to-khai":
        return "Tờ khai"
    elif type == "ban-cam-ket":
        return "Bản cam kết"
    elif type == "giay-cam-ket" or type == "cam-ket":
        return "Giấy cam kết"
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
