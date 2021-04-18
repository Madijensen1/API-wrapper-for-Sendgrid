#import relevent libraries
import sendgrid
import os
import base64
import mimetypes
import ntpath
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition

class NewEmail(object):
	"""
	Represents a new email to be sent.
	"""
	def __init__(self, sender):
		"""
		Initialises the sender of the email.
		"""
		self.sender = sender

	def _createEmail(self, address_to, message, emailSubject):
		"""
		sets up the email and returns a Mail object.

		address_to: string - the address you want to email
		message: string - email body in plain text
		emailSubject: string - subject of the email
		"""
		from_email = Email(self.sender)
		to_email = To(address_to)
		subject = emailSubject
		content = Content("text/plain", message)
		#creates Mail object from sendgrid api
		mail = Mail(from_email, to_email, subject, content)
		return mail

	def _getFileName(self, filePath):
		"""
		Returns the filename of the attachment from the full file path.

		filePath: string - file path located on drive
		"""
		head, tail = ntpath.split(filePath)
		return tail or ntpath.basename(head)
	
	def _createAttachment(self, filePath):
		"""
		Creates and returns an attachment object, sets the disposition as 'attachment'.

		filePath: string - file path located on drive
		"""
		#encode attachment
		with open(filePath, 'rb') as f:
			data = f.read()
		encoded_file = base64.b64encode(data).decode()

		name = self._getFileName(filePath)
		#create attachment object
		attachedFile = Attachment()
		attachedFile.file_content = FileContent(encoded_file)
		attachedFile.file_name = FileName(name)
		attachedFile.file_type = FileType(mimetypes.guess_type(name)[0])
		attachedFile.disposition = Disposition('attachment')

		return attachedFile

	def send(self, address_to, message, emailSubject = "Automated Email", attachmentFilePath = None):
		"""
		Builds the API call and HTTP request, sends email.

		address_to: string - the address you want to email
		message: string - email body in plain text
		emailSubject: string - subject of the email
		attachment: string - file path located on drive

		"""
		mail = self._createEmail(address_to, message, emailSubject)
		if attachmentFilePath != None:
			mail.attachment = self._createAttachment(attachmentFilePath)
		sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
		response = sg.send(mail)
		if response.status_code == 202:
			print("Email sent")
		else:
			print("Email not sent. Please check error codes below - ")
			print(response.status_code)
			print(response.headers)

thismail = NewEmail("madi.jensen@hotmail.com")
thismail.send(address_to="madi.jensen@hotmail.com", message="hey, just wondering how your holiday was? we went there last year and we had a great time! thanks,Mum", attachmentFilePath="C:/Users/madij/Desktop/learn code/Deferit Intern/SoftwareEngineerIntern.pdf")