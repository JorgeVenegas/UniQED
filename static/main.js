var nav = document.getElementById("navbar-nav");
var navlinks = nav.getElementsByClassName("nav-link");
var current = document.getElementById("current")

for (var i = 0; i < navlinks.length; i++) {
  if (navlinks[i].innerHTML == current.innerHTML) {
    navlinks[i].className += " active";
  }
};

let forms = document.getElementsByTagName("form");

for (let i = 0; i < forms.length; i++) {
  forms[i].autocomplete = "off";
}

var sidebar = document.getElementById("sidebar");

if (sidebar != null) {
  var sidebarlinks = sidebar.getElementsByClassName("nav-link");

  var actual = document.getElementById("actual")

  if (actual != null) {
    for (var i = 0; i < sidebarlinks.length; i++) {

      if (sidebarlinks[i].getAttribute('data-bs-name') == actual.innerHTML) {
        sidebarlinks[i].className += " active";
      }
    };
  }
}


var eventDescriptionModal = document.getElementById('eventDescriptionModal')

if (eventDescriptionModal != null) {
  eventDescriptionModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    var id = button.getAttribute('data-bs-id');

    var title = document.getElementById('eventTitle' + id);
    var date = document.getElementById('eventDate' + id);
    var time = document.getElementById('eventTime' + id);
    var description = document.getElementById('eventDescription' + id);

    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var eventTitle = eventDescriptionModal.querySelector('.eventModalTitle');
    var eventDate = eventDescriptionModal.querySelector('.eventModalDate');
    var eventTime = eventDescriptionModal.querySelector('.eventModalTime');
    var eventDescription = eventDescriptionModal.querySelector('.eventModalDescription');

    eventTitle.textContent = title.innerHTML;
    eventDate.textContent = date.innerHTML;
    eventTime.textContent = time.innerHTML;
    eventDescription.textContent = description.innerHTML;

    document.getElementById('deleteEvent').setAttribute('action', "/delete/events/" + id);

  })
}

var noteDescriptionModal = document.getElementById('noteDescriptionModal')

if (noteDescriptionModal != null) {
  noteDescriptionModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    var id = button.getAttribute('data-bs-id');

    var date = document.getElementById('noteDate' + id);
    var title = document.getElementById('noteTitle' + id);
    var description = document.getElementById('noteDescription' + id);

    var noteDate = noteDescriptionModal.querySelector('.noteModalDate');
    var noteTitle = noteDescriptionModal.querySelector('.noteModalTitle');
    var noteDescription = noteDescriptionModal.querySelector('.noteModalDescription');

    noteDate.textContent = date.innerHTML;
    noteTitle.textContent = title.innerHTML;
    noteDescription.textContent = description.innerHTML;

    document.getElementById('deleteNote').setAttribute('action', "/delete/notes/" + id);
  })
}


var addLessonModal = document.getElementById('addLessonModal')

if (addLessonModal != null) {
  addLessonModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    var course = button.getAttribute('data-bs-course');
    var chapter = button.getAttribute('data-bs-chapter');

    document.getElementById('addLesson').setAttribute('action', "/course/" + course + "/" + chapter + "/addLesson");
  })
}

var chaptersAccordion = document.getElementById('chapters')

if (chaptersAccordion != null) {
  var firstChapter = chaptersAccordion.querySelector("button")
  var firstChapterCollapsed = chaptersAccordion.querySelector(".accordion-collapse")

  firstChapter.setAttribute("areia-expandend", "true")

  firstChapter.classList.remove("collapsed")
  firstChapterCollapsed.classList.add("show")
}

var lessonsAccordion = document.getElementById('lessons')

if (lessonsAccordion != null) {
  var firstLesson = lessonsAccordion.querySelector("button")
  var firstLessonCollapsed = lessonsAccordion.querySelector(".accordion-collapse")

  firstLesson.setAttribute("areia-expandend", "true")

  firstLesson.classList.remove("collapsed")
  firstLessonCollapsed.classList.add("show")
}

