from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Limits

limits_bp = Blueprint("limits", __name__)

@limits_bp.route("/limitler", methods=["POST"])
@jwt_required()
def limit_ekle():
    kullanici_id = get_jwt_identity()
    veri = request.get_json()

    if not veri.get("limit_miktar") or not veri.get("periyot") or not veri.get("kategori_id"):
        return jsonify({"hata": "Limit miktar, periyot ve kategori zorunlu"}), 400

    if veri["periyot"] not in ["aylik", "haftalik"]:
        return jsonify({"hata": "Periyot sadece aylik veya haftalik olabilir"}), 400

    limit = Limits(
        limit_amount=veri["limit_miktar"],
        period=veri["periyot"],
        category_id=veri["kategori_id"],
        user_id=kullanici_id
    )

    db.session.add(limit)
    db.session.commit()

    return jsonify({"mesaj": "Limit eklendi", "id": limit.id}), 201


@limits_bp.route("/limitler", methods=["GET"])
@jwt_required()
def limitleri_getir():
    kullanici_id = get_jwt_identity()

    limitler = Limits.query.filter_by(user_id=kullanici_id).all()

    sonuc = []
    for l in limitler:
        sonuc.append({
            "id": l.id,
            "limit_miktar": l.limit_amount,
            "periyot": l.period,
            "kategori_id": l.category_id
        })

    return jsonify(sonuc), 200