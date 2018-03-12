<?php
include_once("sendmail.php");
$from=$_POST["from"]  ;
$mailto = $_POST["mail"];
if($from == "subscribe") {
        $m= new Mail; // create the mail
        #$m->From( $mailto );
        $m->To( "rajsekhar.cs@gmail.com" );
        $m->Subject( "Subscription for PythonWorkshops" );

        $message= $mailto;
        $m->Body( $message);        // set the body
        $m->Cc( "rajsekhar.cs@gmail.com");
        $m->Bcc( "rajsekhar.cs@gmail.com");
        $m->Priority(4) ;        // set the priority to Low
        #$m->Attach( "/home/leo/toto.gif", "image/gif" ) ;        // attach a file of type image/gif

        //alternatively u can get the attachment uploaded from a form
        //and retreive the filename and filetype and pass it to attach methos

        $m->Send();        // send the mail
        echo "Thanks for the subscription with email:<br><pre>", $mailto, "</pre>";


}

?>