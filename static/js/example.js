//set up global variables

var color_vals = ["0","1","2","3","4","5","6","7","8","9",
		              "A","B","C","D","E","F"];

function changeBGColor(){
				var color = "#";
				for (i = 0; i < 6; i++){
								color_index = Math.floor(Math.random()*16);
								color += color_vals[color_index];
				}
				console.log("Changing color to " + color);
				document.body.style.backgroundColor = color;
}