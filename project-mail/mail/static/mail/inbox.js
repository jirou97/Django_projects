
document.addEventListener('DOMContentLoaded', function() {

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', () => {
    let recipients = document.querySelector('#compose-recipients').value;
    let subject = document.querySelector('#compose-subject').value;
    let body = document.querySelector('#compose-body').value;
    if(create_email(recipients,subject,body)){
      load_mailbox('sent');
    }
  });
  // By default, load the inbox
    load_mailbox('inbox');


function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  //document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  get_mailbox(mailbox);
}

function get_mailbox(mailbox){
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      let doc = document.querySelector('#emails-view');
      doc.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
      for (let i = 0 ; i < emails.length ; i ++) {
          let sender = emails[i].sender;
          let subject = emails[i].subject;
          let timestamp = emails[i].timestamp;
          let id = emails[i].id;
          let mail;
          if (emails[i].read) {
              mail = `<div style="background-color: grey;"><div id="email" style="font-size: 20px; "> <b>${sender}</b> ${subject} <a style="float:right;">${timestamp}</a> <a id="email_id" style="display: none">${id}</a></div></div>`;
          } else {
              mail = `<div style="background-color: white;"><div id="email" style="font-size: 20px; "> <b>${sender}</b> ${subject} <a style="float:right;">${timestamp}</a> <a id="email_id" style="display: none">${id}</a></div></div>`;
          }
          doc.innerHTML += mail;
          if (mailbox === "sent"){
              doc.innerHTML += '<hr>';
          }
          if (mailbox !== "sent") {
              if (emails[i].archived === false) {
                  doc.innerHTML += `<div id="archive"><a  class="btn btn-sm btn-outline-primary">Archive</a>  <a id="email_id" style="display: none">${emails[i].id}</a> <a id="email_read" style="display: none">${emails[i].read}</a></div>  <hr>`;

                  document.querySelectorAll('#archive').forEach(function (item) {
                      item.addEventListener('click', function () {
                          update_email(parseInt(item.querySelector('#email_id').innerHTML), true, item.querySelector('#email_read').innerHTML);
                        //document.querySelector('#archive').style.display = 'none';
                          item.innerHTML= 'Added to archives';
                      });
                  });
              } else {
              doc.innerHTML += `<div id="del-archive"><a class="btn btn-sm btn-outline-primary">Remove from archives</a> <a id="email_id" style="display: none">${emails[i].id}</a> <a id="email_read" style="display: none">${emails[i].read}</a></div>  <hr>`;

              document.querySelectorAll('#del-archive').forEach(function (item ) {
                  item.addEventListener('click', function () {
                      update_email(parseInt(item.querySelector('#email_id').innerHTML), false, item.querySelector('#email_read').innerHTML);
                      item.innerHTML = 'Deleted from archives';
                  });
              });
          }
          }
        // `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`
    }
      document.querySelectorAll('#email').forEach(function (item){
        item.addEventListener('click',()=>{
          let id= item.querySelector("#email_id").innerHTML;
          get_email(parseInt(id),mailbox);
        });
      });
  });
}

function get_email(id,mailbox){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
        if (email.read === false) {
            update_email(email.id, email.archived, true);
        }
        let doc = document.querySelector('#emails-view');
        doc.innerHTML = `<div id="email_sent" style="font-size: 20px"> <b> From :</b> ${email.sender}</div> `;
        doc.innerHTML += "<div id='email_sent' style='font-size: 20px'> <b> To :</b>";
        if (email.recipients.length === 1 ){
          doc.innerHTML += ` [${email.recipients[0]}] `;
        }
        else {
          for (let i = 0; i < email.recipients.length; i++) {
            if (i === 0) {
              doc.innerHTML += ` [${email.recipients[i]}, `;
            } else if (i !== email.recipients.length - 1) {
              doc.innerHTML += `${email.recipients[i]}, `;
            } else {
              doc.innerHTML += `${email.recipients[i]}] </div>`;
            }
          }
        }
        doc.innerHTML += `<div id='email_sent' style='font-size: 20px'> <b> Subject :</b> ${email.subject}</div> `;
        doc.innerHTML += `<div id='email_sent' style='font-size: 20px'> <b> Timestamp :</b> ${email.timestamp}</div> </div> `;

        doc.innerHTML += `<hr>`;
        doc.innerHTML += ` <div id='email_sent' style='font-size: 20px'> ${email.body}</div> `;
        doc.innerHTML += `<hr>`;
        if(mailbox !== "sent"){
            doc.innerHTML += `<div><a id="reply" class="btn btn-sm btn-outline-primary" >Reply</a></div>`;

            document.querySelector('#reply').addEventListener('click', function() {
                document.querySelector('#emails-view').style.display = 'none';
                document.querySelector('#compose-view').style.display = 'block';

                // Clear out composition fields
                document.querySelector('#compose-recipients').value = email.sender;
                if( !email.subject.includes("Re : ")){
                    document.querySelector('#compose-subject').value = `Re : ${email.subject}`;
                }else{
                    document.querySelector('#compose-subject').value = `${email.subject}`;
                }
                document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote : ${email.body}`;
              });
        }

  });
}
  function create_email(recipients,subject,body){
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        return result.message === "Email sent successfully.";
    });
  }

  function update_email(id,archived,read){
    if( archived === "true"){
        archived = true;
    }if( archived === "false"){
        archived = false;
    }if( read === "true"){
        read = true;
    }if( read === "false"){
        read = false;
    }
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: archived,
            read: read
        })
      }).then(_ =>
          {});
  }

});

