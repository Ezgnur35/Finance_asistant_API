from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Transaction
from sqlalchemy import extract

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/rapor/aylik", methods=["GET"])
@jwt_required()
def aylik_rapor():
    kullanici_id = get_jwt_identity()

    yil = request.args.get("yil", type=int)
    ay = request.args.get("ay", type=int)

    if not yil or not ay:
        return jsonify({"hata": "Yıl ve ay zorunlu"}), 400

    islemler = Transaction.query.filter(
        Transaction.user_id == kullanici_id,
        extract("year", Transaction.date) == yil,
        extract("month", Transaction.date) == ay
    ).all()

    toplam_gelir = sum(i.amount for i in islemler if i.type == "gelir")
    toplam_gider = sum(i.amount for i in islemler if i.type == "gider")
    tasarruf = toplam_gelir - toplam_gider

    kategoriler = {}
    for i in islemler:
        kid = i.category_id
        if kid not in kategoriler:
            kategoriler[kid] = {"gelir": 0, "gider": 0}
        kategoriler[kid][i.type] += i.amount

    return jsonify({
        "yil": yil,
        "ay": ay,
        "toplam_gelir": toplam_gelir,
        "toplam_gider": toplam_gider,
        "tasarruf": tasarruf,
        "kategorilere_gore": kategoriler
    }), 200