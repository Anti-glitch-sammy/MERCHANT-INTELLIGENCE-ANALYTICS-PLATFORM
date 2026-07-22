from typing import Optional
import datetime
import enum

from sqlalchemy import DateTime, Enum, Float, ForeignKeyConstraint, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class BalesStatus(str, enum.Enum):
    OPEN = 'OPEN'
    FILLED = 'FILLED'
    EXPIRED = 'EXPIRED'
    LOCKED = 'LOCKED'
    PROCESSING = 'PROCESSING'
    SHIPPED = 'SHIPPED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True, autoincrement=True)
    request_id: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    initial_price: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('current_timestamp()'))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('current_timestamp()'))
    estemate_cost: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text('0'))
    delivery_days: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text('30'))
    modify_type: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text('0'))
    free_delivery: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text('0'))
    estemate_modify_type: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text('1'))
    extra_charge_status: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text('0'))
    modify_by: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text('0'))
    sku_attr: Mapped[str] = mapped_column(String(200), nullable=False)
    sku_id: Mapped[str] = mapped_column(String(200), nullable=False)
    push_to_delivery: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text('0'))
    pushed_on: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    merchant_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    items: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    price: Mapped[Optional[str]] = mapped_column(String(255))
    platform: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'pending'"))
    item_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    quantity: Mapped[Optional[int]] = mapped_column(INTEGER(11), server_default=text('1'))
    otp: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    link: Mapped[Optional[str]] = mapped_column(String(255))
    order_from: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    fifthPicture: Mapped[Optional[str]] = mapped_column(String(200))
    fourthPicture: Mapped[Optional[str]] = mapped_column(String(200))
    slug: Mapped[Optional[str]] = mapped_column(String(255))
    initial_estemate_cost: Mapped[Optional[str]] = mapped_column(String(255))
    merchantSlug: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    modify_price: Mapped[Optional[str]] = mapped_column(String(255))
    estemate_modify: Mapped[Optional[str]] = mapped_column(String(200))
    extra_changes_reference: Mapped[Optional[str]] = mapped_column(String(255))
    selected_color: Mapped[Optional[str]] = mapped_column(String(255))
    selected_size: Mapped[Optional[str]] = mapped_column(String(200))
    product_id: Mapped[Optional[str]] = mapped_column(String(255))
    logistics_service_name: Mapped[Optional[str]] = mapped_column(String(255))
    tracking_id: Mapped[Optional[str]] = mapped_column(String(255))


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        Index('link', 'link', unique=True),
        Index('link_10', 'link', unique=True),
        Index('link_11', 'link', unique=True),
        Index('link_12', 'link', unique=True),
        Index('link_13', 'link', unique=True),
        Index('link_14', 'link', unique=True),
        Index('link_15', 'link', unique=True),
        Index('link_16', 'link', unique=True),
        Index('link_17', 'link', unique=True),
        Index('link_18', 'link', unique=True),
        Index('link_19', 'link', unique=True),
        Index('link_2', 'link', unique=True),
        Index('link_20', 'link', unique=True),
        Index('link_21', 'link', unique=True),
        Index('link_22', 'link', unique=True),
        Index('link_23', 'link', unique=True),
        Index('link_24', 'link', unique=True),
        Index('link_25', 'link', unique=True),
        Index('link_26', 'link', unique=True),
        Index('link_27', 'link', unique=True),
        Index('link_28', 'link', unique=True),
        Index('link_29', 'link', unique=True),
        Index('link_3', 'link', unique=True),
        Index('link_30', 'link', unique=True),
        Index('link_31', 'link', unique=True),
        Index('link_32', 'link', unique=True),
        Index('link_33', 'link', unique=True),
        Index('link_34', 'link', unique=True),
        Index('link_35', 'link', unique=True),
        Index('link_36', 'link', unique=True),
        Index('link_37', 'link', unique=True),
        Index('link_38', 'link', unique=True),
        Index('link_39', 'link', unique=True),
        Index('link_4', 'link', unique=True),
        Index('link_40', 'link', unique=True),
        Index('link_41', 'link', unique=True),
        Index('link_42', 'link', unique=True),
        Index('link_43', 'link', unique=True),
        Index('link_44', 'link', unique=True),
        Index('link_45', 'link', unique=True),
        Index('link_46', 'link', unique=True),
        Index('link_47', 'link', unique=True),
        Index('link_48', 'link', unique=True),
        Index('link_49', 'link', unique=True),
        Index('link_5', 'link', unique=True),
        Index('link_50', 'link', unique=True),
        Index('link_51', 'link', unique=True),
        Index('link_52', 'link', unique=True),
        Index('link_53', 'link', unique=True),
        Index('link_54', 'link', unique=True),
        Index('link_55', 'link', unique=True),
        Index('link_56', 'link', unique=True),
        Index('link_57', 'link', unique=True),
        Index('link_58', 'link', unique=True),
        Index('link_6', 'link', unique=True),
        Index('link_7', 'link', unique=True),
        Index('link_8', 'link', unique=True),
        Index('link_9', 'link', unique=True),
        Index('products_created_by', 'createdBy'),
        Index('products_product_type_id', 'productTypeId'),
        Index('products_status', 'status'),
        Index('products_sub_category_id', 'subCategoryId'),
        Index('products_supplier_id', 'supplierId')
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True, autoincrement=True)
    supplierId: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    subCategoryId: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    oldPrice: Mapped[float] = mapped_column(Float, nullable=False)
    productTypeId: Mapped[int] = mapped_column(INTEGER(11), nullable=False, comment='Product type within the subcategory (e.g. Phone, Smart Watch under Smart Devices).')
    isSpecial: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text('0'))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    images: Mapped[Optional[str]] = mapped_column(LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text('1'))
    deletedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    relistPriceCapPercent: Mapped[Optional[float]] = mapped_column(Float, comment='Max allowed markup % for re-list. Null = use global default.')
    relistMinQuantity: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='Min buyable quantity for re-list offers. Null = use global default.')
    platform: Mapped[Optional[str]] = mapped_column(String(255))
    link: Mapped[Optional[str]] = mapped_column(String(255), comment='Source/crawled product URL; unique when set (app-enforced where required).')
    createdBy: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='Admin user ID who created the product (e.g. via save-crawled).')
    currency: Mapped[Optional[str]] = mapped_column(String(10), server_default=text("'¥'"), comment='Currency symbol / code for the product price (e.g. ¥, $, ₦).')
    productAttributes: Mapped[Optional[str]] = mapped_column(LONGTEXT, comment='JSON product attributes/spec metadata (stored as string; parsed on read).')
    packageInfo: Mapped[Optional[str]] = mapped_column(LONGTEXT, comment='JSON package metadata (stored as string; parsed on read).')
    rate: Mapped[Optional[float]] = mapped_column(Float, comment='Product rating score from source marketplace.')
    positiveFeedbackRate: Mapped[Optional[float]] = mapped_column(Float, comment='Positive feedback percentage from source marketplace.')
    reviewsNumber: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='Number of product reviews on source marketplace.')
    prices: Mapped[Optional[str]] = mapped_column(LONGTEXT, comment='JSON array of price objects (stringify on save; parse on read).')
    evaluatePanelSummary: Mapped[Optional[str]] = mapped_column(LONGTEXT, comment='JSON evaluate panel summary (stringify on save; parse on read).')
    shippingFee: Mapped[Optional[float]] = mapped_column(Float, comment='Per-unit shipping fee (e.g. total shipping fee divided by quantity).')
    moq: Mapped[Optional[float]] = mapped_column(Float, comment='Minimum order quantity.')
    originalPrice: Mapped[Optional[float]] = mapped_column(Float, comment="Supplier's original price before markup — used for margin/cost tracking.")

    bales: Mapped[list['Bales']] = relationship('Bales', back_populates='products')


class Suppliers(Base):
    __tablename__ = 'suppliers'
    __table_args__ = (
        Index('clubCode', 'clubCode', unique=True),
        Index('clubCode_10', 'clubCode', unique=True),
        Index('clubCode_11', 'clubCode', unique=True),
        Index('clubCode_12', 'clubCode', unique=True),
        Index('clubCode_13', 'clubCode', unique=True),
        Index('clubCode_14', 'clubCode', unique=True),
        Index('clubCode_15', 'clubCode', unique=True),
        Index('clubCode_16', 'clubCode', unique=True),
        Index('clubCode_17', 'clubCode', unique=True),
        Index('clubCode_18', 'clubCode', unique=True),
        Index('clubCode_19', 'clubCode', unique=True),
        Index('clubCode_2', 'clubCode', unique=True),
        Index('clubCode_20', 'clubCode', unique=True),
        Index('clubCode_3', 'clubCode', unique=True),
        Index('clubCode_4', 'clubCode', unique=True),
        Index('clubCode_5', 'clubCode', unique=True),
        Index('clubCode_6', 'clubCode', unique=True),
        Index('clubCode_7', 'clubCode', unique=True),
        Index('clubCode_8', 'clubCode', unique=True),
        Index('clubCode_9', 'clubCode', unique=True),
        Index('marketId', 'marketId')
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True, autoincrement=True)
    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    userName: Mapped[Optional[str]] = mapped_column(String(255))
    marketId: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    image: Mapped[Optional[str]] = mapped_column(Text)
    profile: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text('1'))
    year: Mapped[Optional[str]] = mapped_column(String(255))
    returnRate: Mapped[Optional[float]] = mapped_column(Float)
    rate: Mapped[Optional[float]] = mapped_column(Float)
    supplierType: Mapped[Optional[str]] = mapped_column(String(255))
    medal: Mapped[Optional[str]] = mapped_column(String(255))
    cityId: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    clubCode: Mapped[Optional[str]] = mapped_column(String(32), comment='Public club/serial code from client (e.g. 001); unique when set.')


class Bales(Base):
    __tablename__ = 'bales'
    __table_args__ = (
        ForeignKeyConstraint(['productId'], ['products.id'], ondelete='CASCADE', onupdate='CASCADE', name='bales_ibfk_1'),
        Index('bales_product_id', 'productId'),
        Index('bales_product_id_status', 'productId', 'status'),
        Index('bales_status', 'status')
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True, autoincrement=True)
    productId: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    quantity: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    slot: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    oldPrice: Mapped[float] = mapped_column(Float, nullable=False)
    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    deliveryFee: Mapped[float] = mapped_column(Float, nullable=False)
    totalDeliveryFee: Mapped[float] = mapped_column(Float, nullable=False)
    isSpecial: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text('0'), comment='Whether this bale is a special / featured offer.')
    restartedCount: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text('0'), comment='Increments on each successful POST /bale/:id/restart.')
    cycle: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text('1'), comment='Pool cycle; increments on each restart.')
    filled: Mapped[Optional[int]] = mapped_column(INTEGER(11), server_default=text('0'))
    filledSlot: Mapped[Optional[int]] = mapped_column(INTEGER(11), server_default=text('0'))
    baleId: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[BalesStatus]] = mapped_column(Enum(BalesStatus, values_callable=lambda cls: [member.value for member in cls]), server_default=text("'OPEN'"))
    endIn: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    shipmentId: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    currency: Mapped[Optional[str]] = mapped_column(String(10), server_default=text("'¥'"), comment='Currency symbol / code for the bale price (e.g. ¥, $, ₦). Inherited from product on creation.')
    originalPrice: Mapped[Optional[float]] = mapped_column(Float, comment="Supplier's original price before markup — used for margin/cost tracking")
    createdBy: Mapped[Optional[int]] = mapped_column(INTEGER(11), comment='FK to adminUsers – the admin who created this bale')
    startedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='When the bale pool window started; defaults to creation time.')
    prices: Mapped[Optional[str]] = mapped_column(LONGTEXT, comment='JSON array of { price, min, max } tiers by slot index (stringify on save; parse on read).')

    products: Mapped['Products'] = relationship('Products', back_populates='bales')
