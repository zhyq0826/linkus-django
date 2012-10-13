from django.db import connection, transaction


def update(table,data,id):
    
    cursor = connection.cursor()
    sql =' UPDATE '+table['table']

    sql+=','.join("set %s='%s "%(k,v) for k,v in data.items())

    sql+=' where id='+id

    # Data modifying operation - commit required
    cursor.execute(sql)
    transaction.commit_unless_managed()



# def dictfetchall(cursor):
#     "Returns all rows from a cursor as a dict"
#     desc = cursor.description
#     return [
#         dict(zip([col[0] for col in desc], row))
#         for row in cursor.fetchall()
#     ]


# def dictfetchone(cursor):
# 	"Returns all rows from a cursor as a dict"
#     desc = cursor.description
#     return {
# 		    for row in cursor.fetchone():
# 		    	dict(zip([col[0] for col in desc], row))
#     }
    
