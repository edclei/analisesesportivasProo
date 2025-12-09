from services.db import cursor

def create_account(user_id, name, acc_type='demo', initial_balance=1000.0):
    cur = cursor()
    cur.execute("""      INSERT INTO accounts (name, type, user_id, balance)
      VALUES (%s,%s,%s,%s) RETURNING id, name, type, balance
    """, (name, acc_type, user_id, initial_balance))
    cur.connection.commit()
    return cur.fetchone()

def get_account(account_id):
    cur = cursor()
    cur.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    return cur.fetchone()

def adjust_balance(account_id, delta):
    cur = cursor()
    cur.execute("UPDATE accounts SET balance = balance + %s WHERE id=%s RETURNING balance", (delta, account_id))
    cur.connection.commit()
    return cur.fetchone()
