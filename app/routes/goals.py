from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Goal
from datetime import datetime

goals_bp = Blueprint("goals", __name__)

@goals_bp.route("/hedefler", methods=["POST"])
@jwt_required()
def hedef_ekle():
    kullanici_id = get_jwt_identity()
    veri = request.get_json()

    if not veri.get("baslik") or not veri.get("hedef_miktar") or not veri.get("son_tarih"):
        return jsonify({"hata": "Başlık, hedef miktar ve son tarih zorunlu"}), 400

    hedef = Goal(
        title=veri["baslik"],
        target_amount=veri["hedef_miktar"],
        current_amount=veri.get("mevcut_miktar", 0.0),
        deadline=datetime.strptime(veri["son_tarih"], "%Y-%m-%d"),
        user_id=kullanici_id
    )

    db.session.add(hedef)
    db.session.commit()

    return jsonify({"mesaj": "Hedef eklendi", "id": hedef.id}), 201


@goals_bp.route("/hedefler", methods=["GET"])
@jwt_required()
def hedefleri_getir():
    kullanici_id = get_jwt_identity()

    hedefler = Goal.query.filter_by(user_id=kullanici_id).all()

    sonuc = []
    for h in hedefler:
        sonuc.append({
            "id": h.id,
            "baslik": h.title,
            "hedef_miktar": h.target_amount,
            "mevcut_miktar": h.current_amount,
            "son_tarih": h.deadline.strftime("%Y-%m-%d"),
            "ilerleme": f"%{int((h.current_amount / h.target_amount) * 100)}"
        })

    return jsonify(sonuc), 200