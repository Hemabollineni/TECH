def calculate_fee(hours, vechicle_type):
   if hours <= 0:
       raise ValueError("Hours must be greater than zero.")
   
   if vechicle_type == "2-wheeler":
       return hours * 20
   elif vechicle_type == "4-wheeler":
       return hours * 30
   else: raise ValueError("Invalid vehicle type. Must be '2-wheeler' or '4-wheeler'.")
