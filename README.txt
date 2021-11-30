Inventory Management System Protocol – ISMP 1.0

Protocol Specification November 2021

Prepared for
The University of Texas Dallas, CS 4390
By
Eric Boysen, Ben Nguyen
 
Table of Contents

INTRODUCTION………………………………………………………………………………………………………………………………………………3
USAGE…………………………………………………………………………………………………………………………………………………………………4
TERMINOLOGY…………………………………………………………………………………………………………………………………………………5
MODEL…………………………………………………………………………………………………………………………………………………………………6
FUNCTIONS………………………………………………………………………………………………………………………………………………………7
 
INTRODUCTION
The Inventory Management System Protocol (IMSP) is a two host, application layer protocol which is used to send application messages between a requester (R) and a server (S) regarding the upkeep of inventory management systems on the central server, S, from the remote host, R. The purpose is for R to be able to remotely request for inventory management functions like, data requests, inventory deletion, and inventory updates. 

This will standardize the operation of maintaining proper inventory management across all corporations to enable network engineers to apply previous knowledge of ISMP to any inventory management system.

 
USAGE
IMSP is a request, response protocol, as its general use case is to communicate between a remote host and a central server. In this case a remote host should initiate communication with a central server and make requests for inventory management functions to be executed using the IMSP specifications. This request will include the desired function and server URI followed by a type code or the name parameter in the second line. The server will the send back a response with a status code, URI, and any requested data.

Because IMSP is not used for any real time application, it is generally assumed to be sent over a TCP connection. This ensures that the data is sent reliably to minimize any potential errors in the inventory system. The standard port for a listening TCP server running the IMSP protocol is port 10000. While we do want the reliability of TCP, we do not require a persistent connection or state, so the TCP connection will be closed after each request. This will result in slower response times, but free up room on the server for additional responses to be handled more readily.
 
TERMINOLOGY
Message: the standard PDU of an application layer packet
Packet: the generic name of a unit of data sent over a network protocol
Packet Data Unit (PDU): the unit of encapsulation used by a layer in the TCP/IP stack 
MODEL
IMSP uses a generic message format for simplicity and ease of understanding and readability.
The first line of any message will take the form:
<FUNCTION> <URI>
The <FUNCTION> will contain the desired function name and be used to specify the inventory management function that the user wants to request for the server to execute.
The following line in a message will take the form:
<PARAMETER>
This PARAMETER value is contextual to the function that is being requested. If the user is requesting a GET function, this parameter will be used to determine how they would like their results sorted. If the user is requesting a UPDATE or DELETE function, this parameter will hold the name of the item they would like to access. The UPDATE function will also contain a second parameter with the new quantity. For a server response message, the PARAMETER value will hold the status code of the function.
Finally only response messages will contain the last line: 
<DATA>
A RESPONSE message will contain a blank line after this header, followed by any requested data or a message if the function returns successfully.
 
GET
FORM:
GET <URI>
<CODE_PARAMETER>

Fields:
URI: This will hold the IP address or DNS name of the server that the user is attempting to make a request to. This must be a valid IPv4 or IPv6 address.

CODE_PARAMETER: This will hold a code which corresponds with how the inventory should be sorted in the RESPONSE message
	Codes:
		1 – Sort by Name
		2 – Sort by Quantity
		3 – Sort by Inventory Date

Description:
The GET message is a type of request message. The GET message sends the server a request for the inventory list information and a code for which way to sort it. A successful operation will return a RESPONSE message with status code 200 and the sorted list in the DATA field in ascending order. If the user makes a code request outside of the range [1,3] it will return a RESPONSE message with status code 400.
 


UPDATE
FORM:
UPDATE <URI>
<NAME_PARAMETER> <NUMBER_PARAMETER>

Fields:
URI: This will hold the IP address or DNS name of the server that the user is attempting to make a request to. This must be a valid IPv4 or IPv6 address.

NAME_PARAMETER: This will hold the name of the object that we would like to update the inventory of. If the item does not exist on file yet, it will create a new inventory item.

NUMBER_PARAMETER: This will hold the number that will be set as the new quantity of an inventory item.
Description:
The UPDATE message is a type of request message. The UPDATE function is used to update the current quantity of an inventory item with the name provided in NAME_PARAMETER. If the item exists in the file, its entry will be updated to display the quantity provided in the NUMBER_PARAMETER field. If the item does not exist, a new entry will be added to the server file using the provided NAME_PARAMETER as the name and NUMBER_PARAMETER as the quantity.
 
DELETE
FORM:
DELETE <URI>
<NAME_PARAMETER> 

Fields:
URI: This will hold the IP address or DNS name of the server that the user is attempting to make a request to. This must be a valid IPv4 or IPv6 address.

NAME_PARAMETER: This will hold the name of the object that we would like to delete from the inventory server file. If the item does not exist on file yet, the response message will contain a status code 400.

Description:
The DELETE message is a type of request message. The DELETE function is used to delete a value from the server’s inventory list. The server searches for the list item with a name equal to NAME_PARAMETER and remove it from the inventory file. The response message will contain a 200 code and message upon successful delete or a 400 if the item is not in the inventory
 
RESPONSE
FORM:
RESPONSE <URI>
<PARAMETER>

<DATA>

Fields:
URI: This will hold the IP address or DNS name of the server that the user is attempting to make a request to. This must be a valid IPv4 or IPv6 address.

PARAMETER: This will contain the status code of the function
	Status Codes:
		200 – Function Successful
		300 – Server Error
		400 – Invalid Request
DATA: Data will contain either a message to the user regarding their update or the requested data depending upon the request that was made
Description:
The RESPONSE message is a type of response message. The RESPONSE function is used by the server host exclusively. This message used to relay the status code of a function back to the requester, so that it may handle the status appropriately. It will also contain any requested information or a message about the status of the operation on a 200 status code.
