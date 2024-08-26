from fastapi import FastAPI
from datetime import datetime
import pyodbc
app = FastAPI()
rt_items_db1 = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def root():
    return {"message": "WifiRTdiag"}


@app.get("/signalchk/{items}")
async def read_item(rbunit: str = '0', signal: int = 0):
    print(rbunit, signal)
    # Establish the connection
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=easysql7.passcheck.com;'
        'DATABASE=iTrack;'
        'UID=sa;'
        'PWD=2lkoPP%22'
    )

    cursor = conn.cursor()
    try:

        # Update statement with condition
        update_query = """
        UPDATE TrackerUnits
        SET diagSignal = ?, diagLastSeen = ?, intStatus = 2
        WHERE rbUnit = ?
        """
        now = datetime.now()

        # Execute the update statement
        cursor.execute(update_query, signal, now, rbunit)

        # Commit the transaction
        conn.commit()

        print("Data updated successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return {"message": f"Updated {rbunit} OK"}
#    return rt_items_db1[rbunit : mac + signal]


@app.get("/rtdiag/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
