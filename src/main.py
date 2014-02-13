if __name__ == "__main__":
	print("1 - Facial Transformations Object")
	print("2 - Static Face Object")
	print("3 - Static Space Shuttle Object")
	print("Type an option...")
	option = input(">>> ")
	
	if option == 1:
		from face_move_example import *
	elif option == 2:
                from face_example import *
	elif option == 3:
		from shuttle_example import *
