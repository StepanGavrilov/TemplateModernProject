import uuid


from database.connection import Base  # type: ignore
from sqlalchemy import Boolean, Column, String, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils.types.phone_number import PhoneNumberType  # type: ignore


class Account(Base):  # type: ignore
    """
    Base class for authenticated account
    """
    __tablename__ = "Account"

    id = Column(
        'id',
        UUID(
            as_uuid=True
        ),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True
    )

    username = Column(
        'username',
        String(32),
        nullable=False,
        unique=True,
    )

    password = Column(
        'password',
        String(512),
        nullable=False,
    )

    is_blocked = Column(
        'is_blocked',
        Boolean(),
        nullable=True,
    )

    is_superuser = Column(
        'is_superuser',
        Boolean(),
        nullable=True,
    )

    is_active = Column(
        'is_active',
        Boolean(),
        nullable=True,
    )

    phone_number = Column(
        'phone_number',
        PhoneNumberType(),
        nullable=True,
    )

    country = Column(
        'country',
        String(32),
        nullable=True,
    )

    job = Column(
        'job',
        String(32),
        nullable=True,
    )
    company = Column(
        'company',
        String(32),
        nullable=True,
    )

    age = Column(
        "age",
        SmallInteger,
        nullable=True,
    )
