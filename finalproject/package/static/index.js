function deleteRecipe(recipeId) {
  fetch("/delete-recipe", {
    method: "POST",
    body: JSON.stringify({ recipeId: recipeId }),
  }).then((_res) => {
    window.location.href = "/library";
  });
}


function addFavorite(recipeId) {
  fetch("/add-favorite", {
    method: "POST",
    body: JSON.stringify({ recipeId: recipeId }),
  }).then((_res) => {
    window.location.href = "/library";
  });
}

function gotoRecipe(recipeId) {
 
    window.location.href = "/recipe/"+recipeId;

}


function deleteFavorite(favoriteId) {
  fetch("/delete-favorite", {
    method: "POST",
    body: JSON.stringify({ favoriteId: favoriteId }),
  }).then((_res) => {
    window.location.href = "/favorites";
  });
}

var slideIndex = 0;
showSlides();

function showSlides() {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}
  slides[slideIndex-1].style.display = "block";
  setTimeout(showSlides, 5000); // Change image every 5 seconds
} 

