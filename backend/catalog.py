from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(frozen=True)
class Fabric:
    id: str
    name: str
    category: str
    composition: str
    finish: str
    weight_gsm: int
    width_in: int
    min_yards: int
    price_per_yard: float
    lead_time_days: int
    sustainable: bool
    colorways: tuple[str, ...]
    uses: tuple[str, ...]

    def to_dict(self) -> dict:
        data = asdict(self)
        data["colorways"] = list(self.colorways)
        data["uses"] = list(self.uses)
        return data


CATALOG: tuple[Fabric, ...] = (
    Fabric(
        id="tf-linen-01",
        name="Harbor Washed Linen",
        category="linen",
        composition="100% European flax linen",
        finish="enzyme washed",
        weight_gsm=185,
        width_in=56,
        min_yards=25,
        price_per_yard=14.8,
        lead_time_days=12,
        sustainable=True,
        colorways=("oat", "indigo", "sage", "charcoal"),
        uses=("shirts", "dresses", "home"),
    ),
    Fabric(
        id="tf-cotton-02",
        name="Studio Organic Poplin",
        category="cotton",
        composition="100% GOTS organic cotton",
        finish="soft mercerized",
        weight_gsm=118,
        width_in=58,
        min_yards=40,
        price_per_yard=9.6,
        lead_time_days=9,
        sustainable=True,
        colorways=("white", "ink", "coral", "moss"),
        uses=("shirts", "linings", "uniforms"),
    ),
    Fabric(
        id="tf-denim-03",
        name="Foundry Stretch Denim",
        category="denim",
        composition="97% cotton, 3% elastane",
        finish="rinse ready",
        weight_gsm=340,
        width_in=61,
        min_yards=60,
        price_per_yard=12.4,
        lead_time_days=16,
        sustainable=False,
        colorways=("raw", "mid blue", "washed black"),
        uses=("jeans", "jackets", "workwear"),
    ),
    Fabric(
        id="tf-silk-04",
        name="Atelier Silk Twill",
        category="silk",
        composition="100% mulberry silk",
        finish="print ready",
        weight_gsm=92,
        width_in=45,
        min_yards=15,
        price_per_yard=28.0,
        lead_time_days=18,
        sustainable=False,
        colorways=("ivory", "navy", "ruby"),
        uses=("scarves", "blouses", "occasionwear"),
    ),
    Fabric(
        id="tf-recycled-05",
        name="Loop Recycled Fleece",
        category="knit",
        composition="72% recycled cotton, 28% recycled polyester",
        finish="brushed back",
        weight_gsm=280,
        width_in=63,
        min_yards=50,
        price_per_yard=11.2,
        lead_time_days=14,
        sustainable=True,
        colorways=("heather gray", "forest", "clay", "black"),
        uses=("hoodies", "sweatpants", "loungewear"),
    ),
)


def list_fabrics(
    *,
    category: str | None = None,
    sustainable: bool | None = None,
    max_price: float | None = None,
) -> list[dict]:
    fabrics: Iterable[Fabric] = CATALOG
    if category:
        fabrics = (item for item in fabrics if item.category == category.lower())
    if sustainable is not None:
        fabrics = (item for item in fabrics if item.sustainable is sustainable)
    if max_price is not None:
        fabrics = (item for item in fabrics if item.price_per_yard <= max_price)
    return [item.to_dict() for item in fabrics]


def get_fabric(fabric_id: str) -> dict | None:
    for item in CATALOG:
        if item.id == fabric_id:
            return item.to_dict()
    return None


def estimate_quote(items: list[dict], destination: str = "domestic") -> dict:
    subtotal = 0.0
    normalized_items = []
    for item in items:
        fabric = get_fabric(str(item["fabric_id"]))
        if fabric is None:
            raise ValueError(f"Unknown fabric: {item['fabric_id']}")
        yards = max(int(item.get("yards", fabric["min_yards"])), fabric["min_yards"])
        line_total = yards * float(fabric["price_per_yard"])
        subtotal += line_total
        normalized_items.append(
            {
                "fabric_id": fabric["id"],
                "name": fabric["name"],
                "yards": yards,
                "line_total": round(line_total, 2),
            }
        )

    shipping_rate = 0.08 if destination == "international" else 0.035
    shipping = subtotal * shipping_rate
    service_fee = 35.0 if subtotal else 0.0
    total = subtotal + shipping + service_fee
    return {
        "items": normalized_items,
        "subtotal": round(subtotal, 2),
        "shipping": round(shipping, 2),
        "service_fee": round(service_fee, 2),
        "total": round(total, 2),
    }
