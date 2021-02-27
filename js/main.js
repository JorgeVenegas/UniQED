const navAppear = () => {
  const burguer = document.querySelector(".nav-hamburguer");
  const nav = document.querySelector("nav");

  burguer.addEventListener("click", () => {
    nav.classList.toggle("nav-active");
  });
};

navAppear();