from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Category

categories_bp = Blueprint("categories", __name__)

@categories_bp.route("/kategoriler", methods=["POST"])
@jwt_required()
def kategori_ekle():
    kullanici_id = get_jwt_identity()
    veri = request.get_json()

    if not veri.get("isim"):
        return jsonify({"hata": "Kategori ismi zorunlu"}), 400

    kategori = Category(
        name=veri["isim"],
        user_id=kullanici_id
    )

    db.session.add(kategori)
    db.session.commit()

    return jsonify({"mesaj": "Kategori eklendi", "id": kategori.id}), 201


@categories_bp.route("/kategoriler", methods=["GET"])
@jwt_required()
def kategorileri_getir():
    kullanici_id = get_jwt_identity()

    kategoriler = Category.query.filter_by(user_id=kullanici_id).all()

    sonuc = []
    for k in kategoriler:
        sonuc.append({
            "id": k.id,
            "isim": k.name
        })

    return jsonify(sonuc), 200