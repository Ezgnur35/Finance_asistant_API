from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Transaction, Category

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/transactions", methods=["POST"])
@jwt_required()
def islem_ekle():
    kullanici_id = get_jwt_identity()
    veri = request.get_json()

    if not veri.get("miktar") or not veri.get("tur") or not veri.get("kategori_id"):
        return jsonify({"hata": "Miktar, tür ve kategori zorunlu"}), 400

    if veri["tur"] not in ["gelir", "gider"]:
        return jsonify({"hata": "Tür sadece gelir veya gider olabilir"}), 400

    islem = Transaction(
        amount=veri["miktar"],
        description=veri.get("aciklama", ""),
        type=veri["tur"],
        category_id=veri["kategori_id"],
        user_id=kullanici_id
    )

    db.session.add(islem)
    db.session.commit()

    return jsonify({"mesaj": "İşlem eklendi"}), 201


@transactions_bp.route("/transactions", methods=["GET"])
@jwt_required()
def islemleri_getir():
    kullanici_id = get_jwt_identity()

    islemler = Transaction.query.filter_by(user_id=kullanici_id).all()

    sonuc = []
    for i in islemler:
        sonuc.append({
            "id": i.id,
            "miktar": i.amount,
            "aciklama": i.description,
            "tur": i.type,
            "kategori_id": i.category_id,
            "tarih": i.date.strftime("%Y-%m-%d %H:%M")
        })

    return jsonify(sonuc), 200


@transactions_bp.route("/transactions/<int:id>", methods=["DELETE"])
@jwt_required()
def islem_sil(id):
    kullanici_id = get_jwt_identity()

    islem = Transaction.query.filter_by(id=id, user_id=kullanici_id).first()

    if not islem:
        return jsonify({"hata": "İşlem bulunamadı"}), 404

    db.session.delete(islem)
    db.session.commit()

    return jsonify({"mesaj": "İşlem silindi"}), 200