import mysql.connector as connector
from datetime import datetime
conn=connector.connect(host='localhost',user='root',passwd='Tr1v@ndrum')
crsr=conn.cursor()
crsr.execute('use funmovies;')
crsr.execute('select * from users;')
base_date = datetime(1, 1, 1)
for rec in crsr:
    print(rec[0],rec[1],rec[2],rec[3], rec[4],sep=',')
def insertMovies():
    name=input('Enter Movie Name: ')
    genre=input('Enter Genre: ')
    releasedate=input('Enter Release Date(YYYY-MM-DD): ')
    duration=int(input('Enter Duration(in minutes): '))
    crsr.execute('select * from showtime;')
    print('Showtimes in Database:')
    print(f'{"ShowID":<10}{"Date":<20}{"Time":<20}')
    print("="*50)
    for rec in crsr:
        date= rec[1].strftime('%Y-%m-%d')
        datetime_val = base_date + rec[2]
        time_val = datetime_val.time()
        time = time_val.strftime('%H:%M:%S')
        print(f'{rec[0]:<10}{date:<20}{time:<20}')
        print("-"*50)
    showtimeid=input('Enter ShowtimeID: ')
    crsr.execute('select max(movieid) from movies;')
    movieid='m'+str(int(crsr.fetchone()[0][1:])+1)
    crsr.execute('INSERT INTO movies VALUES (%s, %s, %s, %s, %s, %s);', (movieid, name, genre, releasedate, duration, showtimeid))
    conn.commit()
    print('Movie Added Successfully')

def insertTheatre():
    name=input('Enter Theatre Name: ')
    location=input('Enter Location: ')
    capacity=int(input('Enter Capacity: '))
    crsr.execute('select max(theatreid) from theatre where theatreid like concat("%", %s, "%");', (name,))
    tid= crsr.fetchone()[0]
    theatreid=0
    for ch in tid:
        if ch.isdigit():
            theatreid=int(ch)
    theatreid=name+str(theatreid+1)
    crsr.execute('INSERT INTO theatre VALUES (%s, %s, %s, %s);', (theatreid, name, location, capacity))
    conn.commit()
    print('Theatre Added Successfully')

def insertShowtime():
    date=input('Enter Date(YYYY-MM-DD): ')
    time=input('Enter Time(HH:MM:SS): ')
    crsr.execute('select max(showid) from showtime;')
    showid='st'+str(int(crsr.fetchone()[0][2:])+1)
    crsr.execute('INSERT INTO showtime VALUES (%s, %s, %s);', (showid, date, time,))
    conn.commit()
    print('Showtime Added Successfully')

def insertSeats():
    crsr.execute('select * from theatre;')
    print('Theatres in Database:')
    print(f'{"TheatreID":<10}{"Name":<20}{"Location":<20}{"Capacity":<20}')
    print("="*70)
    for rec in crsr:
        print(f'{rec[0]:<10}{rec[1]:<20}{rec[2]:<20}{rec[3]:<20}')
        print("-"*70)
    theatreid=input('Enter TheatreID: ')
    types=input('Enter Type: ')
    price=int(input('Enter Price: '))
    crsr.execute('select max(seatid) from seats;')
    seatid='s'+str(int(crsr.fetchone()[0][1:])+1)
    crsr.execute('INSERT INTO seats VALUES (%s, %s, %s,false, %s);', (seatid, types, price,theatreid,))
    conn.commit()
    print('Seat Added Successfully')

def displayMovies():
    crsr.execute('select distinct movies.* from movies, plays where movies.movieid=plays.movieid')
    print(f'{"MovieID":<10}{"Name":<20}{"Genre":<20}{"Release Date":<20}{"Duration(in minutes)":<20}')
    print("="*90)
    for rec in crsr:
        print(f'{rec[0]:<10}{rec[1]:<20}{rec[2]:<20}{rec[3].strftime("%Y-%m-%d"):<20}{rec[4]:<20}')
        print("-"*90)

def bookTickets(userid):
    #try:
        print('Movies Running Today:')
        displayMovies()
        movieid=input('Enter the movieid: ')
        crsr.execute('select name from movies where movieid=%s and %s in (select movieid from plays);',(movieid,movieid,))
        moviename=crsr.fetchone()[0]
        crsr.execute('select theatre.* from theatre, plays where movieid=%s and plays.theatreid=theatre.theatreid;',(movieid,))
        print('Select Theatre:')
        print(f'{"TheatreID":<10}{"Name":<20}{"Location":<20}{"Capacity":<20}')
        print("="*70)
        for rec in crsr:
            print(f'{rec[0]:<10}{rec[1]:<20}{rec[2]:<20}{rec[3]:<20}')
            print("-"*70)
        theatreid=input('Enter the theatreid: ')
        crsr.execute('select name, location from theatre where theatreid=%s and %s in (select theatreid from plays where movieid=%s);',(theatreid,theatreid,movieid,))
        for rec in crsr:
            theatrename=rec[0]
            location=rec[1]
        print('Select Show:')
        crsr.execute('select showtime.showid, showtime.date, showtime.time from showtime, movies where movies.movieid=%s and showtime.showid=movies.showtime;',(movieid,))
        print(f'{"ShowID":<10}{"Date":<20}{"Time":<20}')
        print("="*50)
        for rec in crsr:
            date= rec[1].strftime('%Y-%m-%d')
            datetime_val = base_date + rec[2]  # Add timedelta to base date
            time_val = datetime_val.time()  # Extract the time from the datetime object
            time = time_val.strftime('%H:%M:%S')  # Format time to string
            print(f'{rec[0]:<10}{date:<20}{time:<20}')
            print("-"*50)
        showtimeid=input('Enter the showid: ')
        crsr.execute('select date, time from showtime where showid=%s;',(showtimeid,))
        for rec in crsr:
            if rec[0]==None or rec[1]==None:
                print('Invalid ShowID')
                return
            date= rec[0].strftime('%Y-%m-%d')
            datetime_val = base_date + rec[1]
            time_val = datetime_val.time()
            time = time_val.strftime('%H:%M:%S')
        crsr.execute('select seatid, type, price from seats where theatreid=%s;',(theatreid,))
        print('Select Seat:')
        print(f'{"SeatID":<10}{"Type":<20}{"Price":<20}')
        print("="*50)
        for rec in crsr:
            print(f'{rec[0]:<10}{rec[1]:<20}{rec[2]:<20}')
            print("-"*50)
        seatid=input('Enter the seatid: ')
        crsr.execute('select price from seats where seatid=%s;',(seatid,))
        price=crsr.fetchone()[0]
        print()
        print('-'*50)
        print('Ticket Details')
        print('='*50)
        print(f'{"Movie":<20}{moviename:<30}')
        print(f'{"Theatre":<20}{theatrename:<30}')
        print(f'{"Location":<20}{location:<30}')
        print(f'{"Date":<20}{date:<30}')
        print(f'{"Showtime":<20}{time:<30}')
        print(f'{"SeatID":<20}{seatid:<30}')
        print(f'{"Price":<20}{price:<30}')
        print('-'*50)
        print('Select Payment Method: \nCredit Card \nDebit Card \nNet Banking \nUPI')
        payment=input('Enter the payment method: ')
        crsr.execute('select max(paymentid) from payment;')
        paymentid= 'p'+str(int(crsr.fetchone()[0][1:])+1)
        crsr.execute('INSERT INTO payment VALUES (%s, %s, %s, %s);',(paymentid , payment, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), price))
        crsr.execute('select max(ticketid) from ticket;')
        ticketid='t'+str(int(crsr.fetchone()[0][1:])+1)
        crsr.execute('INSERT INTO ticket (ticketid, userid, theatreid, movieid, showid, seatid) VALUES (%s, %s, %s, %s, %s, %s);', (ticketid, userid, theatreid, movieid, showtimeid, seatid))
        crsr.execute('update seats set status=true where seatid=%s;',(seatid,))
        conn.commit()
        print('Ticket Booked Successfully')    
    #except:
        #print('ERROR')

#userid=int(input('Enter UserID: '))
#bookTickets(userid)

def customerAnalysis():
    try:
        crsr.execute('select users.userid, users.name, count(ticket.ticketid) from users, ticket where users.userid=ticket.userid group by users.userid;')
        print('Customer Analysis:')
        print("="*55)
        print(f'{"UserID":<10}{"Name":<20}{"No: of Tickets Booked":<25}')
        print("="*55)
        for rec in crsr:
            print(f'{rec[0]:<10}{rec[1]:<20}{rec[2]:<25}')
            print("-"*55)
    except:
        print('ERROR')
#customerAnalysis()

def login():
    try:
        email=input('Enter EmailID: ')
        password=input('Enter Password: ')
        crsr.execute('select userid from users where email=%s and password=%s;',(email,password))
        userid=crsr.fetchone()[0]
        return userid
    except:
        print("Login Failed! Kindly check your credentials or register to continue")

def comingSoon():
    crsr.execute('select * from movies where releasedate>curdate();')
    print(f'{"MovieID":<10}{"Name":<20}{"Genre":<20}{"Release Date":<20}{"Duration(in minutes)":<20}')
    print("="*90)
    for rec in crsr:
        print(f'{rec[0]:<10}{rec[1]:<20}{rec[2]:<20}{rec[3].strftime("%Y-%m-%d"):<20}{rec[4]:<20}')
        print("-"*90)

def viewTickets(userid):
    try:
        crsr.execute('select ticket.ticketid, movies.name, theatre.name, showtime.date, showtime.time, seats.type from ticket, movies, theatre, showtime, seats where ticket.userid=%s and ticket.movieid=movies.movieid and ticket.theatreid=theatre.theatreid and ticket.showid=showtime.showid and ticket.seatid=seats.seatid;',(userid,))
        print(f'{"TicketID":<10}{"Movie":<20}{"Theatre":<20}{"Date":<20}{"Time":<20}{"Seat Type":<20}')
        print("="*120)
        for rec in crsr:
            date= rec[3].strftime('%Y-%m-%d')
            datetime_val = base_date + rec[4]
            time_val = datetime_val.time()
            time = time_val.strftime('%H:%M:%S')
            print(f'{rec[0]:<10}{rec[1]:<20}{rec[2]:<20}{date:<20}{time:<20}{rec[5]:<20}')
        print("-"*120)
    except:
        print('ERROR') 
def deleteTicket(userid):
    print('My Tickets:')
    viewTickets(userid)
    ticketid=input('Enter TicketID to cancel: ')
    crsr.execute('update seats set status=false where seatid in (select seatid from ticket where ticketid=%s and userid=%s);',(ticketid,userid,))
    crsr.execute('delete from ticket where ticketid=%s and userid=%s;',(ticketid,userid,))
    conn.commit()
    print('Ticket Cancelled Successfully')

def deleteMovies():
    try:
        print('Movies in Database:')
        crsr.execute('select * from movies;')
        print(f'{"MovieID":<10}{"Name":<20}{"Genre":<20}{"Release Date":<20}{"Duration(in minutes)":<20}')
        print("="*90)
        for rec in crsr:
            print(f'{rec[0]:<10}{rec[1]:<20}{rec[2]:<20}{rec[3].strftime("%Y-%m-%d"):<20}{rec[4]:<20}')
            print("-"*90)
        movieid=input('Enter MovieID to delete: ')
        crsr.execute('delete from movies where movieid=%s;',(movieid,))
        if crsr.rowcount==0:
            print('Invalid MovieID')
            return
        conn.commit()
        print('Movie Deleted Successfully')
    except:
        print('ERROR')

def deleteTheatre():
    try:
        print('Theatres in Database:')
        crsr.execute('select * from theatre;')
        print(f'{"TheatreID":<10}{"Name":<20}{"Location":<20}{"Capacity":<20}')
        print("="*70)
        for rec in crsr:
            print(f'{rec[0]:<10}{rec[1]:<20}{rec[2]:<20}{rec[3]:<20}')
            print("-"*70)
        theatreid=input('Enter TheatreID to delete: ')
        crsr.execute('delete from theatre where theatreid=%s;',(theatreid,))
        conn.commit()
        print('Theatre Deleted Successfully')
    except:
        print('ERROR')

def deleteShowtime():
    try:
        print('Showtimes in Database:')
        crsr.execute('select * from showtime;')
        print(f'{"ShowID":<10}{"Date":<20}{"Time":<20}')
        print("="*50)
        for rec in crsr:
            date= rec[1].strftime('%Y-%m-%d')
            datetime_val = base_date + rec[2]
            time_val = datetime_val.time()
            time = time_val.strftime('%H:%M:%S')
            print(f'{rec[0]:<10}{date:<20}{time:<20}')
            print("-"*50)
        showid=input('Enter ShowID to delete: ')
        print('The following movies are scheduled for this show, kindly change their showtime before deleting this showtime')
        crsr.execute('select name from movies where showtime=%s;',(showid,))
        for rec in crsr:
            st= input('Enter the new showtime for the movie '+rec[0]+': ')
            crsr.execute('update showtime set showid=%s where showid=%s;',(st,showid,))
        crsr.execute('delete from showtime where showid=%s;',(showid,))
        conn.commit()
        print('Showtime Deleted Successfully')
        
    except:
        print('ERROR')

def deleteSeats():
    try:
        print('Seats in Database:')
        crsr.execute('select seatid, type, price, theatreid from seats;')
        print(f'{"SeatID":<10}{"Type":<20}{"Price":<20}{"TheatreID":<20}')
        print("="*70)
        for rec in crsr:
            print(f'{rec[0]:<10}{rec[1]:<20}{rec[2]:<20}{rec[3]:<20}')
            print("-"*70)
        seatid=input('Enter SeatID to delete: ')
        print('There are tickets booked for this seat, ticktes will be cancelled and the user will be refunded')
        crsr.execute('delete from ticket where seatid=%s;',(seatid,))
        print('Tickets Cancelled Successfully')
        crsr.execute('delete from seats where seatid=%s;',(seatid,))
        conn.commit()
        print('Seat Deleted Successfully')
    except:
        print('ERROR')

print("="*50)  
print(" "*10,"FunMovies Database System")
print("="*50)
while True:
    print('1. Enter as a User ')
    print('2. Enter as an Admin ')
    print('3. Exit')
    num=int(input('Enter your choice: '))
    if num==1:
        while True:
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice=int(input("Enter your choice: "))
            if choice==1:
                userid=login()
                if userid!=None:
                    print('Login Successful!')
                    print("="*50)
                    crsr.execute('select name from users where userid=%s;',(userid,))
                    print(" "*13,'Welcome ',crsr.fetchone()[0],'!')
                    while True:
                        print("1. Show Movies that are currently running \n2. Book Tickets \n3. Show Movies that are coming soon \n4. View my Tickets \n5. Cancel ticket \n0. Logout")
                        opt=int(input("Enter your choice: "))
                        if opt==1:
                            displayMovies()
                        elif opt==2:
                            bookTickets(userid)
                        elif opt==3:
                            comingSoon()
                        elif opt==4:
                            viewTickets(userid)
                        elif opt==5:
                            deleteTicket(userid)
                        elif opt==0:
                            break
                        else:
                            print('Invalid Choice, Try Again!')
            elif choice==2:
                name=input('Enter Name: ')
                email=input('Enter EmailID: ')
                phone=input('Enter Phone Number: ')
                password=input('Enter Password: ')
                crsr.execute('select max(userid) from users;')
                userid=int(crsr.fetchone()[0])+1
                crsr.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s,%s);', (userid, name, email, phone, password,0,))
                conn.commit()
                print('Registration Successful!')
            elif choice==3:
                print('Thank You!')
                break
            else:
                print('Invalid Choice, Try Again!')
    elif num==2:
        print("="*50)
        print(" "*15,"Admin Panel")
        print("="*50)
        while True:
            print("1. Insert Movies")
            print("2. Delete Movies")
            print("3. Insert Theatre")
            print("4. Delete Theatre")
            print("5. Insert Showtime")
            print("6. Delete Showtime")
            print("7. Insert Seats")
            print("8. Delete Seats")
            print("9. Customer Analysis")
            print("0. Exit")
            choice=int(input("Enter your choice: "))
            if choice==1:
                insertMovies()
            elif choice==2:
                deleteMovies()
            elif choice==3:
                insertTheatre()
            elif choice==4:
                deleteTheatre()
            elif choice==5:
                insertShowtime()
            elif choice==6:
                deleteShowtime()
            elif choice==7:
                insertSeats()
            elif choice==8:
                deleteSeats()
            elif choice==9:
                customerAnalysis()
            elif choice==0:
                print('Logging out as Admin')
                print("="*50)
                print()
                break
            else:
                print('Invalid Choice, Try Again!')
    elif num==3:
        break