litestarのpolyfactoryでGeometryを扱う
========================================

.. post:: 2025-03-23
   :tags: Python, geometry, litestar, polyfactory, sqlalchemy
   :author: sion908
   :language: ja
   :location: blog/2025

はじめに
--------

litestar+sqlalchemyを用いてアプリの開発をしており、テストコードを書く際に、モックデータということで、litestarの派生ライブラリ？であるpolyfactoryを使った。
この時、geoalchemy2を使っているのだが、簡単には生成してくれなかったので、記事として残しておく。

スクリプト
----------

.. code-block:: python

   import random
   from typing import Any, Callable
   from advanced_alchemy.base import UUIDBase
   from sqlalchemy import Column, Integer, String
   from geoalchemy2 import Geometry
   from geoalchemy2.functions import ST_X, ST_Y
   from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
   from sqlalchemy.orm import Mapped, mapped_column


   # Geometry型を含むSQLAlchemyモデル
   import random
   from typing import Any, Callable
   from advanced_alchemy.base import UUIDBase
   from sqlalchemy import Column, Integer, String
   from geoalchemy2 import Geometry
   from geoalchemy2.functions import ST_X, ST_Y
   from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
   from sqlalchemy.orm import Mapped, mapped_column


   # Geometry型を含むSQLAlchemyモデル
   class Location(UUIDBase):
       __tablename__ = "locations"
       
       id = Column(Integer, primary_key=True)
       name = Column(String(100), nullable=False)
       location: Mapped[str] = mapped_column(Geometry("POINT", srid=4326), nullable=True)
       
       def __repr__(self):
           return f"<Location(id={self.id}, name={self.name}, location=(<{ST_Y(self.location)}> <{ST_X(self.location)}>)))>"


   class LocationFactory(SQLAlchemyFactory[Location]):
       __model__ = Location

       @classmethod
       def get_sqlalchemy_types(cls) -> dict[Any, Callable[[], Any]]:
           types = super().get_sqlalchemy_types()
           types[Geometry] = lambda: f'POINT({random.uniform(-180, 180)} {random.uniform(-90, 90)})'
           return types
       
       @classmethod
       def location(cls) -> str:
           return cls.get_sqlalchemy_types()[Geometry]()

   # 使用例
   def demo_mock_creation():
       loc = [LocationFactory().build() for _ in range(10)]
       for l in loc:
           assert type(l) == Location
           assert l.location is not None

   # デモ実行
   if __name__ == "__main__":
       demo_mock_creation()

何をやったのか
--------------

追加したのは、``LocationFactory`` における ``get_sqlalchemy_types`` の

.. code-block:: python

   types[Geometry] = lambda: f'POINT({random.uniform(-180, 180)} {random.uniform(-90, 90)})'

の部分。
ついでに、null許容だったのですが、モックでは値を必ず入れて欲しかったので

.. code-block:: python

       @classmethod
       def location(cls) -> str:
           return cls.get_sqlalchemy_types()[Geometry]()

を追記しています。

litestarのコミュニティにきいたところ

.. code-block:: text

   SQLA factory is a bit different to others in the sense there's an extra translation layer from column type to python type that needs to be done in factory.
   -- SQLA（SQLAlchemy）のファクトリーは他のものとは少し異なっていて、カラムの型をPythonの型に変換するための追加の変換レイヤーがファクトリー内に必要になるんだ。

   Can you try overriding https://polyfactory.litestar.dev/reference/factories/sqlalchemy_factory.html#polyfactory.factories.sqlalchemy_factory.SQLAlchemyFactory.get_sqlalchemy_types to map this type to callable that returns a random value for this column type?

とのこと。
そりゃ生成されないわけです。

元々のエラー
------------

.. code-block:: sh

   AttributeError: 'Geometry' object has no attribute 'impl'
   It looks like this stems from polyfactory trying to infer a python_type from the Geometry column, which isn't supported by GeoAlchemy2's Geometry type.

implがないとのことですね。
AIに聞いても全然解決策の提示はしてもらえませんでした。

参考
----

`https://polyfactory.litestar.dev/reference/factories/sqlalchemy_factory.html#polyfactory.factories.sqlalchemy_factory.SQLAlchemyFactory.get_sqlalchemy_types <https://polyfactory.litestar.dev/reference/factories/sqlalchemy_factory.html#polyfactory.factories.sqlalchemy_factory.SQLAlchemyFactory.get_sqlalchemy_types>`_

追記
----

ドキュメント更新していただけました
ありがとうございます
`https://github.com/litestar-org/polyfactory/pull/671 <https://github.com/litestar-org/polyfactory/pull/671>`_
