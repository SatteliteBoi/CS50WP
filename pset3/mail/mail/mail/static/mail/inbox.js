document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
 
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#heading').style.display = 'block';
  console.log("compose email");
  // Clear out composition fields
  document.querySelector('#compose-recipients').disabled=false;
  document.querySelector('#compose-subject').disabled=false;
  document.querySelector('#compose-body').disabled=false;
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelector("#compose-form").onsubmit = sendemail;
  document.querySelector('#sendemailbuttonid').style.display = 'block';
  if(document.querySelector('#fromsent')!==null){
    fromsent = document.getElementById("fromsent");
    fromsent.value=fromsent.defaultValue;
  }
  if(document.querySelector('#archiveButtonId')!==null){
    document.querySelector('#archiveButtonId').style.display="none";
  }
  if(document.querySelector('#replybuttonid')!==null){
    document.querySelector('#replybuttonid').style.display="none";
  }
  document.querySelector('#fromsent').display="block";
  if(document.querySelector('#viewfrom')!==null){
    document.querySelector('#viewfrom').display="none";
  }
}

function sendemail() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
  return false;
}

function view_email(id, mailbox){
  fetch(`/emails/${Number(id)}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);
    console.log(`/emails/${Number(id)}`);
  // ... do something else with email ...
    compose_email();
      document.querySelector('#compose-recipients').value = email.recipients;
      document.querySelector('#compose-subject').value = email.subject;
      document.querySelector('#compose-body').value = email.body;
      document.querySelector('#compose-recipients').disabled=true;
      document.querySelector('#compose-subject').disabled=true;
      document.querySelector('#compose-body').disabled=true;
      document.querySelector('#sendemailbuttonid').style.display = 'none';
      fetch(`/emails/${Number(id)}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })

    console.log(`email.archived: ${email.archived}`)

    let archiveButtonId =  "archiveButtonId"; 
    button = document.getElementById(archiveButtonId);
    if(button == null)
    {
      console.log("Creating archiveButtonId")
      button = document.createElement("button");
      button.setAttribute("class", "btn btn-primary");
      button.setAttribute("id", archiveButtonId);
      button.style.display="none";
      document.querySelector('#compose-view').appendChild(button);
    }

    console.log(`email.archived: ${email.archived}`)
    button.innerHTML= email.archived!==true ? "Archive" : "Unarchive";
    button.onclick = () =>{
      fetch(`/emails/${Number(id)}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: email.archived!=true
        })
      })
    }
    replybutton=document.getElementById('replybuttonid');
    if(replybutton==null){
      console.log("Creating replybutton")
      replybutton = document.createElement("button");
      replybutton.innerHTML = "Reply"
      replybutton.setAttribute("class", "btn btn-primary");
      replybutton.setAttribute("id", 'replybuttonid');
      replybutton.style.display="none";
      document.querySelector('#compose-view').appendChild(replybutton);
    }
  
      replybutton.onclick = () =>{
        compose_email();
        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = "Re:" + email.subject;
        document.querySelector('#compose-body').value = "On " + email.timestamp + " " + email.sender + " wrote: " + email.body + "\n\n";
      }

      if(mailbox!=="sent"){
        button.style.display="inline-block";
        replybutton.style.display="inline-block";
        fromsent = document.getElementById("fromsent");
        fromsent.value = email.sender;
        console.log(`sender:${email.sender}`)
      }
      document.querySelector('#heading').style.display = 'none';
  });
}
function load_mailbox(mailbox) {

  console.log("load_mailbox")
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  mailboxname = mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailboxname}</h3>`;
  
  //fetch mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);

    // ... do something else with emails ...
      emails.forEach(element => {
        wrapper = document.createElement("div");
        div = document.createElement("div");


        from = document.createElement("div");
        from.innerHTML="From: "+element.sender;
        from.style.textalign="left";
        div.appendChild(from);

        subject = document.createElement("div");
        div.appendChild(subject);
        subject.innerHTML="Subject: "+element.subject;
        subject.style.textalign="center";
        
        timestamp = document.createElement("div");
        div.appendChild(timestamp);
        timestamp.innerHTML=element.timestamp;
        timestamp.style.textalign="left";
        
        div.setAttribute("style", "width: 100%; display: inline; height: 40%;");
        from.setAttribute("class", "from");
        subject.setAttribute("class", "subject");
        timestamp.setAttribute("class", "timestamp");

        button = document.createElement("button");
        button.setAttribute("class", "openemailbutton");
        button.appendChild(div);
        button.class = "email";
        button.onclick = function(){
          view_email(element.id, mailbox);
        }
        if(element.read==true){ 
          button.setAttribute("style", "background: white;")
        }
        document.querySelector('#emails-view').appendChild(button)
      });
  });
}