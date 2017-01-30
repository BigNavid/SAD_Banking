// Get all the keys from document
var keys = document.querySelectorAll('#atm span');
var operators = ['+', '-', 'x', '÷'];
var isCardNumEntered = false;
var isPasswordEntered = false;
var cardNumber;
var password;

// Add onclick event to all the keys and perform operations
for(var i = 0; i < keys.length; i++) {
	keys[i].onclick = function(e) {
		// Get the input and button values
        var context = document.querySelector('#context');
		var input = document.querySelector('#context_input');
		var inputVal = input.innerHTML;
		var btnVal = this.innerHTML;
		
		// Now, just append the key values (btnValue) to the input string and finally use javascript's eval function to get the result
		// If eval key is pressed, calculate and display the result
		if(btnVal == 'تایید') {
            if(inputVal != '' & !isCardNumEntered){
                isCardNumEntered = true;
                isPasswordEntered= false;
                cardNumber = inputVal;
                input.innerHTML = '';
                context.innerHTML = 'لطفا کلمه عبور خود را وارد کنید.';

            }
            else if(inputVal != '' & !isPasswordEntered){
                isPasswordEntered = true;
                isCardNumEntered = false;
                password = inputVal;
                post('', {cardNumber: cardNumber, password: password});
            }
		}

		else if(btnVal == 'انصراف'){
            location.reload();
        }

        else if(btnVal == 'تصحیح'){
            input.innerHTML = '';
        }

		// if any other key is pressed, just append it
		else {
			input.innerHTML += btnVal;
		}
		
		// prevent page jumps
		e.preventDefault();
	} 
}

function post(path, params) {
    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.querySelector('#form_temp');

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}