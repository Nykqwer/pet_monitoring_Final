from mysql.connector import connect, Error

connection = None

try:
    connection = connect(
        host="localhost",
        user="root",
        password="",
        database="pet_monitordb",
        port="3306"
    )
    
    cursor = connection.cursor()
    print("Connected to the database!")
    
    
    def checkUser(username, password=None):
        cmd = f"Select count(username) from login where username='{username}' and BINARY password='{password}'"
        cursor.execute(cmd)
        cmd = None
        a = cursor.fetchone()[0] >= 1
        return a
    
    
        # Add a pet_info
    def add_petInfo(name, breed, age, weight, h_con, encoded_image):
        try:
            query = "INSERT INTO pet_info (name, breed, age, weight, heal_con, image) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (name, breed, age, weight, h_con, encoded_image)
            cursor.execute(query, values)
            connection.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def get_petInfo():
        try:
            cmd = "SELECT name, breed, age, weight, heal_con, image FROM pet_info;"
            
            # Ensure cursor is properly defined and handled
            with connection.cursor() as cursor:
                cursor.execute(cmd)

                # Fetch the results
                result = cursor.fetchall()

                # Check if the result is empty
                if not result:
                    return False

                # If there are rows, return the first one
                return result[0]
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def add_activity(type_act, duration, DT_act, note):
            try:
                # Assuming cursor and connection are properly defined and connected
                query = "INSERT INTO activity (type_act, duration, DT_act, note) VALUES (%s, %s, %s, %s)"
                values = (type_act, duration, DT_act, note)

                # Execute the query
                cursor.execute(query, values)

                # Commit the transaction
                connection.commit()

                # Return True indicating success
                return True

            except Exception as e:
                # Log the error instead of just printing it
                print(f"Error: {e}")

                # Return False indicating failure
                return False
            
    def get_activity():
        try:
            cmd = "SELECT id, type_act, duration, DT_act, note FROM activity;"
            cursor.execute(cmd)

            # Fetch the results
            result = cursor.fetchall()

            # Check if the result is empty
            if not result:
                return False

            return result
        except Exception as e:
            print(f"Error: {e}")
            return None
                    
    def update_activity(id, type_act, duration, DT_act, note):
        cmd = "UPDATE activity SET type_act = %s, duration = %s, DT_act = %s, note = %s WHERE id = %s"
        cursor.execute(cmd, (type_act, duration, DT_act, note, id))
        connection.commit()
        if cursor.rowcount == 0:
            return False
        return True  
        
        # Delete a activity
    def delete_activity(id):
        cmd = f"delete from activity where id='{id}';"
        cursor.execute(cmd)
        connection.commit() 
        if cursor.rowcount == 0:
            return False
        return True
    
     #Add Health
    def add_health(event, w_event, DT_heal, medication):
        try:
            # Assuming cursor and connection are properly defined and connected
            query = "INSERT INTO health (event, w_event, DT_heal, medication) VALUES (%s, %s, %s, %s)"
            values = (event, w_event, DT_heal, medication)

            # Execute the query
            cursor.execute(query, values)

            # Commit the transaction
            connection.commit()

            # Return True indicating success
            return True

        except Exception as e:
            # Log the error instead of just printing it
            print(f"Error in health: {e}")

            # Return False indicating failure
            return False
        

        # Get health data
    def get_health():
        try:
            cmd = "SELECT id, event, w_event, DT_heal, medication FROM health;"
            cursor.execute(cmd)

            # Fetch the results
            result = cursor.fetchall()

            if not result:  # If the result is an empty list, there are no rows
                return False

            return result
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def delete_health(id):
        cmd = "DELETE FROM health WHERE id = %s;"
        print(cmd)
        cursor.execute(cmd, (id,))
        connection.commit()  # Commit changes
        if cursor.rowcount == 0:
            return False
        return True
        
    
    # update health
    def update_health(id,event,w_event,DT_heal, medication):
        cmd = f"update health set event = '{event}',w_event= '{w_event}', DT_heal = '{DT_heal}', medication = '{medication}' where id = '{id}';"
        cursor.execute(cmd)
        connection.commit()
        if cursor.rowcount == 0:
            return False
        return True

        
    
except Error as e:
    print(f"Error: {e}")