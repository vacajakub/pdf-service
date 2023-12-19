import io

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool


async def insert_document(db: AsyncConnectionPool, num_pages: int) -> int:
    async with db.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """INSERT INTO documents (status, n_pages) VALUES (%s, %s) RETURNING id;""",
                ("processing", num_pages),
            )
            res = await cur.fetchone()

            return res["id"]


# !!! normally image should be saved in CDN and only an url in db !!! this is only for the assignment
async def insert_page(db: AsyncConnectionPool, document_id: int, page_number: int, image_data: io.BytesIO):
    async with db.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """INSERT INTO pages (document_id, document_page, image)
                   VALUES (%s, %s, %s) 
                   ON CONFLICT DO NOTHING;""",
                (document_id, page_number, image_data.getvalue()),
            )


async def mark_document_as_done(db: AsyncConnectionPool, document_id: int):
    async with db.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """UPDATE documents SET status = %s WHERE id=%s;""",
                ("done", document_id),
            )


async def get_document_db(db: AsyncConnectionPool, document_id: int) -> dict:
    async with db.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """SELECT status, n_pages FROM documents WHERE id=%s;""",
                (document_id,),
            )
            return await cur.fetchone()


async def get_page_data(db: AsyncConnectionPool, document_id: int, page_number: int) -> dict:
    async with db.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """SELECT image FROM pages WHERE document_id=%s AND document_page=%s;""",
                (document_id, page_number),
            )
            return await cur.fetchone()
