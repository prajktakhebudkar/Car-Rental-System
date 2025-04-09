import datetime
from enum import Enum
from typing import List, Dict, Optional


class RentalBasis(Enum):
    """Enum representing different rental time periods."""
    HOURLY = 1
    DAILY = 2
    WEEKLY = 3


class Car:
    """Class representing a car in the rental system."""
    
    def __init__(self, car_id: str, model: str, price_hourly: float, price_daily: float, price_weekly: float):
        """Initialize a new Car object.
        
        Args:
            car_id: Unique identifier for the car
            model: Car model name
            price_hourly: Hourly rental price
            price_daily: Daily rental price
            price_weekly: Weekly rental price
        """
        self.car_id = car_id
        self.model = model
        self.price_hourly = price_hourly
        self.price_daily = price_daily
        self.price_weekly = price_weekly
        self.available = True
        self.rental_start_time = None
        self.rental_basis = None
    
    def __str__(self) -> str:
        """Return string representation of the car."""
        status = "Available" if self.available else "Not Available"
        return f"Car ID: {self.car_id} | Model: {self.model} | Status: {status}"


class Customer:
    """Class representing a customer in the rental system."""
    
    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        """Initialize a new Customer object.
        
        Args:
            customer_id: Unique identifier for the customer
            name: Customer name
            email: Customer email
            phone: Customer phone number
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.rented_cars = []
        self.rental_history = []
    
    def __str__(self) -> str:
        """Return string representation of the customer."""
        return f"Customer ID: {self.customer_id} | Name: {self.name} | Email: {self.email}"


class Rental:
    """Class representing a rental transaction."""
    
    def __init__(self, rental_id: str, customer: Customer, cars: List[Car], rental_basis: RentalBasis, 
                 start_time: datetime.datetime):
        """Initialize a new Rental object.
        
        Args:
            rental_id: Unique identifier for the rental
            customer: Customer who is renting
            cars: List of cars being rented
            rental_basis: Basis of rental (hourly, daily, weekly)
            start_time: Start time of the rental
        """
        self.rental_id = rental_id
        self.customer = customer
        self.cars = cars
        self.rental_basis = rental_basis
        self.start_time = start_time
        self.end_time = None
        self.bill_amount = 0.0
    
    def calculate_bill(self, return_time: datetime.datetime = None) -> float:
        """Calculate the bill amount based on rental duration and basis.
        
        Args:
            return_time: Optional time when cars were returned. Defaults to current time.
        
        Returns:
            float: The calculated bill amount
        """
        if return_time:
            self.end_time = return_time
        elif not self.end_time:
            self.end_time = datetime.datetime.now()
        
        rental_duration = self.end_time - self.start_time
        
        if self.rental_basis == RentalBasis.HOURLY:
            hours = max(1, int(rental_duration.total_seconds() / 3600))
            self.bill_amount = sum(car.price_hourly * hours for car in self.cars)
            duration_str = f"{hours} hour(s)"
        
        elif self.rental_basis == RentalBasis.DAILY:
            days = max(1, int(rental_duration.total_seconds() / (24 * 3600)))
            self.bill_amount = sum(car.price_daily * days for car in self.cars)
            duration_str = f"{days} day(s)"
        
        elif self.rental_basis == RentalBasis.WEEKLY:
            weeks = max(1, int(rental_duration.total_seconds() / (7 * 24 * 3600)))
            self.bill_amount = sum(car.price_weekly * weeks for car in self.cars)
            duration_str = f"{weeks} week(s)"
        
        print(f"Rental duration: {duration_str}")
        
        return self.bill_amount


class Bill:
    """Class representing a bill for a rental."""
    
    def __init__(self, bill_id: str, rental: Rental):
        """Initialize a new Bill object.
        
        Args:
            bill_id: Unique identifier for the bill
            rental: Rental associated with the bill
        """
        self.bill_id = bill_id
        self.rental = rental
        self.amount = rental.calculate_bill()
        self.generated_time = datetime.datetime.now()
        self.paid = False
    
    def mark_as_paid(self):
        """Mark the bill as paid."""
        self.paid = True
    
    def generate_invoice(self) -> str:
        """Generate a readable invoice."""
        rental_basis_str = self.rental.rental_basis.name.lower()
        duration = (self.rental.end_time - self.rental.start_time).total_seconds()
        
        if self.rental.rental_basis == RentalBasis.HOURLY:
            duration_units = max(1, int(duration / 3600))
            unit_str = "hour(s)"
        elif self.rental.rental_basis == RentalBasis.DAILY:
            duration_units = max(1, int(duration / (24 * 3600)))
            unit_str = "day(s)"
        else:
            duration_units = max(1, int(duration / (7 * 24 * 3600)))
            unit_str = "week(s)"
        
        invoice = f"""
        ======= INVOICE =======
        Bill ID: {self.bill_id}
        Customer: {self.rental.customer.name}
        
        Rental Details:
        - Rental ID: {self.rental.rental_id}
        - Rental Basis: {rental_basis_str}
        - Duration: {duration_units} {unit_str}
        - Start Time: {self.rental.start_time.strftime('%Y-%m-%d %H:%M:%S')}
        - End Time: {self.rental.end_time.strftime('%Y-%m-%d %H:%M:%S')}
        
        Cars Rented:
        """
        
        for car in self.rental.cars:
            invoice += f"- Car ID: {car.car_id} | Model: {car.model}\n"
        
        invoice += f"""
        Total Amount: Rs{self.amount:.2f}
        Status: {"Paid" if self.paid else "Unpaid"}
        
        Generated on: {self.generated_time.strftime('%Y-%m-%d %H:%M:%S')}
        =======================
        """
        
        return invoice


class CarRentalSystem:
    """Main class for the car rental system."""
    
    def __init__(self, company_name: str):
        """Initialize a new CarRentalSystem.
        
        Args:
            company_name: Name of the car rental company
        """
        self.company_name = company_name
        self.inventory: Dict[str, Car] = {}
        self.customers: Dict[str, Customer] = {}
        self.rentals: Dict[str, Rental] = {}
        self.bills: Dict[str, Bill] = {}
        self.customer_counter = 0
        self.rental_counter = 0
        self.bill_counter = 0
        
        # Initialize with 50 Maruti Suzuki Baleno cars
        self._initialize_inventory()
    
    def _initialize_inventory(self):
        """Initialize the inventory with 50 Maruti Suzuki Baleno cars."""
        for i in range(1, 51):
            car_id = f"BAL{i:03d}"
            car = Car(car_id, "Maruti Suzuki Baleno", 200.0, 1000.0, 4750.0)
            self.inventory[car_id] = car
        
        print(f"Inventory initialized with 50 Maruti Suzuki Baleno cars.")
    
    def add_car(self, car: Car) -> bool:
        """Add a car to the inventory.
        
        Args:
            car: Car object to add
            
        Returns:
            bool: True if addition successful, False otherwise
        """
        if car.car_id in self.inventory:
            print(f"Car with ID {car.car_id} already exists in inventory.")
            return False
        
        self.inventory[car.car_id] = car
        print(f"Car with ID {car.car_id} added to inventory successfully.")
        return True
    
    def register_customer(self, name: str, email: str, phone: str) -> Customer:
        """Register a new customer.
        
        Args:
            name: Customer name
            email: Customer email
            phone: Customer phone number
            
        Returns:
            Customer: The newly registered customer
        """
        self.customer_counter += 1
        customer_id = f"CUST{self.customer_counter:04d}"
        
        customer = Customer(customer_id, name, email, phone)
        self.customers[customer_id] = customer
        
        print(f"\nCustomer registered successfully.")
        print(f"Customer ID: {customer_id}")
        print(f"Name: {name}")
        
        return customer
    
    def display_available_cars(self) -> List[Car]:
        """Display all available cars.
        
        Returns:
            List[Car]: List of available cars
        """
        available_cars = [car for car in self.inventory.values() if car.available]
        
        if not available_cars:
            print("No cars are currently available for rent.")
            return []
        
        print(f"\nAvailable Cars ({len(available_cars)}):")
        print("=" * 50)
        for car in available_cars:
            print(f"{car}")
            print(f"   Hourly Rate: Rs{car.price_hourly:.2f} | Daily Rate: Rs{car.price_daily:.2f} | Weekly Rate: Rs{car.price_weekly:.2f}")
        print("=" * 50)
        
        return available_cars
    
    def display_customers(self):
        """Display all registered customers."""
        if not self.customers:
            print("No customers are registered in the system.")
            return
        
        print(f"\nRegistered Customers ({len(self.customers)}):")
        print("=" * 50)
        for customer in self.customers.values():
            print(f"{customer}")
            if customer.rented_cars:
                print(f"   Currently renting {len(customer.rented_cars)} car(s)")
        print("=" * 50)
    
    def display_rentals(self):
        """Display all active rentals."""
        active_rentals = {rental_id: rental for rental_id, rental in self.rentals.items() 
                         if rental.end_time is None}
        
        if not active_rentals:
            print("No active rentals in the system.")
            return
        
        print(f"\nActive Rentals ({len(active_rentals)}):")
        print("=" * 50)
        for rental_id, rental in active_rentals.items():
            print(f"Rental ID: {rental_id}")
            print(f"Customer: {rental.customer.name}")
            print(f"Cars: {len(rental.cars)}")
            print(f"Start Time: {rental.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Rental Basis: {rental.rental_basis.name}")
            print("-" * 30)
        print("=" * 50)
    
    def find_customer(self, customer_id: str) -> Optional[Customer]:
        """Find a customer by ID.
        
        Args:
            customer_id: ID of the customer to find
            
        Returns:
            Optional[Customer]: Customer object if found, None otherwise
        """
        if customer_id in self.customers:
            return self.customers[customer_id]
        
        print(f"Customer with ID {customer_id} not found.")
        return None
    
    def find_available_cars(self, count: int) -> List[Car]:
        """Find a specific number of available cars.
        
        Args:
            count: Number of cars needed
            
        Returns:
            List[Car]: List of available cars up to the requested count
        """
        available_cars = [car for car in self.inventory.values() if car.available]
        
        if len(available_cars) < count:
            print(f"Only {len(available_cars)} cars are available out of {count} requested.")
            return []
        
        return available_cars[:count]
    
    def parse_datetime(self, datetime_str: str) -> datetime.datetime:
        """Parse datetime string in the format 'YYYY-MM-DD HH:MM'.
        
        Args:
            datetime_str: Datetime string
            
        Returns:
            datetime.datetime: Parsed datetime object
        """
        try:
            return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        except ValueError:
            print("Invalid datetime format. Please use YYYY-MM-DD HH:MM")
            raise
    
    def rent_cars(self, customer_id: str, car_count: int, rental_basis: RentalBasis, 
                 start_time: datetime.datetime) -> Optional[Rental]:
        """Rent cars to a customer.
        
        Args:
            customer_id: ID of the customer renting cars
            car_count: Number of cars to rent
            rental_basis: Basis of rental (hourly, daily, weekly)
            start_time: Start time of the rental
            
        Returns:
            Optional[Rental]: Rental object if successful, None otherwise
        """
        customer = self.find_customer(customer_id)
        if not customer:
            return None
        
        cars_to_rent = self.find_available_cars(car_count)
        if not cars_to_rent:
            return None
        
        # Generate rental ID
        self.rental_counter += 1
        rental_id = f"R{self.rental_counter:04d}"
        
        # Create rental
        rental = Rental(rental_id, customer, cars_to_rent, rental_basis, start_time)
        self.rentals[rental_id] = rental
        
        # Update car status
        for car in cars_to_rent:
            car.available = False
            car.rental_start_time = start_time
            car.rental_basis = rental_basis
        
        # Update customer rentals
        customer.rented_cars.extend(cars_to_rent)
        
        basis_str = rental_basis.name.lower()
        print(f"\nCars rented successfully on a {basis_str} basis.")
        print(f"Rental ID: {rental_id}")
        print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Number of cars rented: {len(cars_to_rent)}")
        
        return rental
    
    def return_cars(self, rental_id: str, return_time: datetime.datetime) -> Optional[Bill]:
        """Return rented cars and generate bill.
        
        Args:
            rental_id: ID of the rental to return
            return_time: Time when cars are returned
            
        Returns:
            Optional[Bill]: Bill object if successful, None otherwise
        """
        if rental_id not in self.rentals:
            print(f"Rental with ID {rental_id} not found.")
            return None
        
        rental = self.rentals[rental_id]
        
        if rental.end_time is not None:
            print(f"Rental with ID {rental_id} has already been returned.")
            return None
        
        rental.end_time = return_time
        
        # Update car status
        for car in rental.cars:
            car.available = True
            car.rental_start_time = None
            car.rental_basis = None
        
        # Update customer rentals
        for car in rental.cars:
            if car in rental.customer.rented_cars:
                rental.customer.rented_cars.remove(car)
        
        rental.customer.rental_history.append(rental)
        
        # Generate bill
        self.bill_counter += 1
        bill_id = f"B{self.bill_counter:04d}"
        bill = Bill(bill_id, rental)
        self.bills[bill_id] = bill
        
        print(f"\nCars returned successfully.")
        print(f"Rental ID: {rental_id}")
        print(f"End Time: {return_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Bill ID: {bill_id}")
        print(f"Amount: ${bill.amount:.2f}")
        
        return bill


def interactive_menu():
    """Interactive menu for the car rental system."""
    car_rental_system = CarRentalSystem("Prachi's Baleno Shop")
    
    while True:
        print("\n" + "=" * 50)
        print(f"Welcome to {car_rental_system.company_name}")
        print("=" * 50)
        print("1. Register New Customer")
        print("2. Rent Cars")
        print("3. Return Cars")
        print("4. View Available Cars")
        print("5. View Customers")
        print("6. View Active Rentals")
        print("7. Exit")
        print("=" * 50)
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == '1':
            # Register new customer
            print("\n--- Register New Customer ---")
            name = input("Enter customer name: ")
            email = input("Enter customer email: ")
            phone = input("Enter customer phone: ")
            
            customer = car_rental_system.register_customer(name, email, phone)
            print(f"Customer registered successfully with ID: {customer.customer_id}")
        
        elif choice == '2':
            # Rent cars
            print("\n--- Rent Cars ---")
            car_rental_system.display_customers()
            
            customer_id = input("Enter customer ID: ")
            customer = car_rental_system.find_customer(customer_id)
            
            if not customer:
                continue
            
            try:
                car_count = int(input("Enter number of cars to rent: "))
                if car_count <= 0:
                    print("Number of cars must be positive.")
                    continue
                
                print("\nRental Basis Options:")
                print("1. Hourly (Rs 200.00 per hour per car)")
                print("2. Daily (Rs 1000.00 per day per car)")
                print("3. Weekly (Rs 4750.00 per week per car)")
                
                basis_choice = input("Choose rental basis (1-3): ")
                
                if basis_choice == '1':
                    rental_basis = RentalBasis.HOURLY
                elif basis_choice == '2':
                    rental_basis = RentalBasis.DAILY
                elif basis_choice == '3':
                    rental_basis = RentalBasis.WEEKLY
                else:
                    print("Invalid choice. Please try again.")
                    continue
                
                start_date_str = input("Enter pickup date and time (YYYY-MM-DD HH:MM): ")
                
                try:
                    start_time = car_rental_system.parse_datetime(start_date_str)
                except ValueError:
                    continue
                
                rental = car_rental_system.rent_cars(customer_id, car_count, rental_basis, start_time)
                
                if rental:
                    print(f"Cars rented successfully. Rental ID: {rental.rental_id}")
            
            except ValueError:
                print("Invalid input. Please enter numeric values where required.")
        
        elif choice == '3':
            # Return cars
            print("\n--- Return Cars ---")
            car_rental_system.display_rentals()
            
            rental_id = input("Enter rental ID: ")
            
            if rental_id not in car_rental_system.rentals:
                print(f"Rental with ID {rental_id} not found.")
                continue
            
            rental = car_rental_system.rentals[rental_id]
            if rental.end_time is not None:
                print(f"Rental with ID {rental_id} has already been returned.")
                continue
            
            return_date_str = input("Enter return date and time (YYYY-MM-DD HH:MM): ")
            
            try:
                return_time = car_rental_system.parse_datetime(return_date_str)
                
                if return_time < rental.start_time:
                    print("Return time cannot be earlier than rental start time.")
                    continue
                
                bill = car_rental_system.return_cars(rental_id, return_time)
                
                if bill:
                    print(bill.generate_invoice())
            
            except ValueError:
                continue
        
        elif choice == '4':
            # View available cars
            car_rental_system.display_available_cars()
        
        elif choice == '5':
            # View customers
            car_rental_system.display_customers()
        
        elif choice == '6':
            # View active rentals
            car_rental_system.display_rentals()
        
        elif choice == '7':
            # Exit
            print("\nThank you for using Swift Wheels Car Rental. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    interactive_menu()