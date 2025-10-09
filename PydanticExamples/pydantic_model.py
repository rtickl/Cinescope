from enum import Enum

from pydantic import BaseModel, Field


class ProductType(str, Enum):
    ELECTRONICS = "Электроника"
    CLOTHING = "Одежда"
    FOOD = "Еда"

class Product(BaseModel):
    name: str = Field(..., description="Название продукта")
    price: float = Field(..., ge=0, description="Цена продукта")
    in_stock: bool = Field(..., description="Есть ли товар в наличии")
    type: ProductType = Field(..., description="Тип продукта")

product = Product(
    name="Наушники APPLE",
    price=24000.0,
    in_stock=True,
    type=ProductType.ELECTRONICS
)

json_data = product.model_dump_json(indent=4)
print(" JSON:\n", json_data)

product_obj = Product.model_validate_json(json_data)

print("\n Объект после десериализации:\n", product_obj)