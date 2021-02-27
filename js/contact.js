const submitForm = () => {
  const formbutton = document.querySelector(".b-submit");
  const form = document.querySelector("#contact-form");

  formbutton.addEventListener("click", () => {
    confirm("Form Sent!");
    form.submit();
  });
};

submitForm();
