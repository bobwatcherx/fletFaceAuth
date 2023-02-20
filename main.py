from flet import *
import cv2
import face_recognition
import json
import os


def main(page:Page):


	nametxt = TextField(label="username")
	jobtxt = TextField(label="you job")


	def registernow(e):
		name_job = f"{nametxt.value} - {jobtxt.value}"
		capture = cv2.VideoCapture(0)
		while True:
			ret,frame  = capture.read()
			cv2.imshow("capture you face",frame)

			# IF YOU PRESS s from YOu Keyboard then save you face
			if cv2.waitKey(1) & 0xFF  == ord("s"):
				image_path = os.path.join("face",f"{name_job}.jpg")
				cv2.imwrite(image_path,frame)
				break

			# AND IF YOU PRESS q then exit from webcam window
			elif cv2.waitKey(1) & 0xFF == ord("q"):
				break
		capture.release()
		cv2.destroyAllWindows()
		# AND RECOGNITION YOU FACE
		encoding = face_recognition.face_encodings(face_recognition.load_image_file(image_path))[0].tolist()
		data = {}
		data[name_job] = {"job":jobtxt.value,"encoding":encoding}

		# AND SAVE TO DATA.json FILE ALL INPUT LIKE NAME JOB AND YOU FACE
		with open("data.json","w") as f:
			json.dump(data,f)
		print("USER IS CREATED GUYS !!!!")
		# AND SHOW SNACKBAR
		page.snack_bar = SnackBar(
			Text("User created Sucess",size=30),
			bgcolor="blue"
			)
		page.snack_bar.open = True
		page.update()


	def loginnow(e):
		capture = cv2.VideoCapture(0)
		while True:
			ret, frame = capture.read()
			cv2.imshow("Capture Wajah", frame)
			if cv2.waitKey(1) & 0xFF == ord('s'):
				cv2.imwrite(f"wajah.jpg", frame)
				break
			elif cv2.waitKey(1) & 0xFF == ord('q'):
				break
		capture.release()
		cv2.destroyAllWindows()
		encoding = face_recognition.face_encodings(face_recognition.load_image_file("wajah.jpg"))
		if len(encoding) > 0:
			encoding = encoding[0]
			with open("data.json","r") as f:
				data = json.load(f)
			for name_job , value in data.items():
				if face_recognition.compare_faces([value['encoding']],encoding)[0]:
					name,job = name_job.split("-")
					print(f"welcome : {name} ({job}) ")
					# SHOW SNACKBAR
					page.snack_bar = SnackBar(
						Text(f"welcome : {name} {job}",size=30),
						bgcolor="green"

						)		
					page.snack_bar.open = True
					page.update()
				else:
					print("You Data is invalid !!!!")
					# SHOW SNACKBAR
					page.snack_bar = SnackBar(
						Text("Data Is invalid"),
						bgcolor="red"

						)		
					page.snack_bar.open = True
					page.update()


		# IF NO FACE IS CAPTURE THE SHOW NOTIF NO FACE DETECTED
		else:
			print("NO FACE DETECTED !!!!!!")
			# SHOW SNACKBAR
			page.snack_bar = SnackBar(
						Text("NO FACE FOUND !!!!!"),
						bgcolor="red"

						)		
			page.snack_bar.open = True
			page.update()	




	page.add(
	Column([
	Text("Face login app",size=30,weight="bold"),
	nametxt,
	jobtxt,

	Row([
		ElevatedButton("Register",
		bgcolor="orange",color="white",
		on_click=registernow
			),
		ElevatedButton("Login",
		bgcolor="blue",color="white",
		on_click=loginnow
			),

		])


	])

	)


flet.app(target=main)
