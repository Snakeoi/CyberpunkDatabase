FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
    "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
    "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Donald", "Sandra",
    "Mark", "Ashley", "Paul", "Kimberly", "Steven", "Emily", "Andrew", "Donna", "Kenneth", "Michelle",
    "George", "Dorothy", "Joshua", "Carol", "Kevin", "Amanda", "Brian", "Melissa", "Edward", "Deborah",
    "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Laura", "Jeffrey", "Sharon", "Ryan", "Cynthia",
    "Jacob", "Kathleen", "Gary", "Amy", "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen",
    "Stephen", "Anna", "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma",
    "Frank", "Samantha", "Benjamin", "Katherine", "Gregory", "Christine", "Raymond", "Debra", "Samuel", "Rachel",
    "Patrick", "Catherine", "Alexander", "Carolyn", "Jack", "Janet", "Dennis", "Ruth", "Jerry", "Maria",
    "Tyler", "Heather", "Aaron", "Diane", "Henry", "Virginia", "Douglas", "Julie", "Peter", "Joyce",
    "Jose", "Victoria", "Adam", "Olivia", "Zachary", "Kelly", "Nathan", "Christina", "Walter", "Lauren",
    "Harold", "Joan", "Kyle", "Evelyn", "Carl", "Judith", "Arthur", "Megan", "Gerald", "Cheryl",
    "Roger", "Andrea", "Keith", "Hannah", "Jeremy", "Martha", "Terry", "Jacqueline", "Lawrence", "Frances",
    "Sean", "Gloria", "Christian", "Ann", "Albert", "Teresa", "Joe", "Kathryn", "Ethan", "Sara",
    "Austin", "Janice", "Jesse", "Jean", "Willie", "Alice", "Billy", "Madison", "Bryan", "Doris",
    "Bruce", "Abigail", "Jordan", "Julia", "Ralph", "Judy", "Roy", "Grace", "Noah", "Denise",
    "Dylan", "Amber", "Eugene", "Marilyn", "Wayne", "Beverly", "Alan", "Danielle", "Juan", "Theresa",
    "Louis", "Sophia", "Russell", "Marie", "Gabriel", "Diana", "Randy", "Brittany", "Philip", "Natalie",
    "Harry", "Isabella", "Vincent", "Charlotte", "Bobby", "Rose", "Johnny", "Alexis", "Logan", "Kayla",
    "Howard", "Lillian", "Martin", "Annette", "Craig", "Savannah", "Stanley", "Brooke", "Curtis", "Faith",
    "Miguel", "Caroline", "Leonard", "Morgan", "Caleb", "Avery", "Theodore", "Hailey", "Shawn", "Jasmine"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez",
    "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes",
    "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero", "Jordan", "Patterson", "Alexander", "Hamilton", "Graham",
    "Reynolds", "Griffin", "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant", "Herrera", "Gibson",
    "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray", "Ford", "Castro", "Marshall", "Owens",
    "Harrison", "Fernandez", "Mcdonald", "Woods", "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Chen",
    "Freeman", "Webb", "Tucker", "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter",
    "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz", "Hunt", "Hicks",
    "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd", "Rose", "Stone", "Salazar", "Fox",
    "Warren", "Mills", "Meyer", "Rice", "Schmidt", "Garza", "Daniels", "Ferguson", "Nichols", "Stephens",
    "Soto", "Weaver", "Ryan", "Gardner", "Payne", "Grant", "Dunn", "Kelley", "Spencer", "Hawkins",
    "Arnold", "Pierce", "Vazquez", "Hansen", "Peters", "Santos", "Hart", "Bradley", "Knight", "Elliott",
    "Cunningham", "Duncan", "Armstrong", "Hudson", "Carroll", "Lane", "Riley", "Andrews", "Alston", "Carr"
]

def get_fullname():
    """
    Generates a random full name by combining a first name and a last name.

    Returns:
        str: A randomly generated full name.
    """
    import random
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return f"{first_name} {last_name}"