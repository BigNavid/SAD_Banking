// Get all the keys from document
var keys = document.querySelectorAll('#atm span');
var isATMSelected = false;
var isCardNumEntered = false;
var isPasswordEntered = false;
var cardNumber;
var password;
var atm_id;
var is_withdraw_cash = false;
var is_deposit_to_credit_card = false;
var to_credit_card;
var is_deposit_to_bank_account = false;
var to_bank_account;
var is_amount_entered = false;
var amount;


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
		    if(inputVal != '' & !isATMSelected){
                isATMSelected = true;
                atm_id = inputVal;
                input.innerHTML = '';
                context.innerHTML = 'لطفا شماره کارت خود را وارد کنید.';
                document.querySelector('#message').innerHTML = ''
            }
            else if(inputVal != '' & !isCardNumEntered){
                isCardNumEntered = true;
                cardNumber = inputVal;
                input.innerHTML = '';
                context.innerHTML = 'لطفا کلمه عبور خود را وارد کنید.';
                document.querySelector('#message').innerHTML = ''
            }
            else if(inputVal != '' & !isPasswordEntered){
                isPasswordEntered = true;
                password = inputVal;
                input.innerHTML = '';
                document.getElementById('right_1').innerHTML = 'برداشت وجه'
                document.getElementById('right_1').className = 'button'
                document.getElementById('right_2').innerHTML = 'انتقال وجه'
                document.getElementById('right_2').className = 'button'
                context.innerHTML = 'لطفا سرویس مورد نظر خود را انتخاب کنید.';
            }
            else if(inputVal != '' & is_withdraw_cash & !is_amount_entered){
                amount = inputVal;
                post('', {atm_id: atm_id, cardNumber: cardNumber, password: password, amount: amount, is_withdraw_cash: is_withdraw_cash, is_deposit_to_credit_card: is_deposit_to_credit_card, is_deposit_to_bank_account: is_deposit_to_bank_account, to_credit_card: to_credit_card, to_bank_account: to_bank_account})
            }
            else if(inputVal != '' & is_deposit_to_credit_card & !is_amount_entered){
                amount = inputVal;
                is_amount_entered = true;
                input.innerHTML = '';
                context.innerHTML = 'لطفا شماره کارت مقصد را وارد کنید.';
            }
            else if(inputVal != '' & is_deposit_to_credit_card & is_amount_entered){
                to_credit_card = inputVal;
                post('', {atm_id: atm_id, cardNumber: cardNumber, password: password, amount: amount, is_withdraw_cash: is_withdraw_cash, is_deposit_to_credit_card: is_deposit_to_credit_card, is_deposit_to_bank_account: is_deposit_to_bank_account, to_credit_card: to_credit_card, to_bank_account: to_bank_account})
            }
            else if(inputVal != '' & is_deposit_to_bank_account & !is_amount_entered){
                amount = inputVal;
                is_amount_entered = true;
                input.innerHTML = '';
                context.innerHTML = 'لطفا شماره حساب مقصد را وارد کنید.';
            }
            else if(inputVal != '' & is_deposit_to_bank_account & is_amount_entered){
                to_bank_account = inputVal;
                post('', {atm_id: atm_id, cardNumber: cardNumber, password: password, amount: amount, is_withdraw_cash: is_withdraw_cash, is_deposit_to_credit_card: is_deposit_to_credit_card, is_deposit_to_bank_account: is_deposit_to_bank_account, to_credit_card: to_credit_card, to_bank_account: to_bank_account})
            }
		}

		else if(btnVal == 'انصراف'){
            location.reload();
        }

        else if(btnVal == 'تصحیح'){
            input.innerHTML = '';
        }

        else if(btnVal =='برداشت وجه'){
            is_withdraw_cash = true;
            document.getElementById('right_1').className = 'button disable'
            document.getElementById('right_2').className = 'button disable'
            input.innerHTML = '';
            context.innerHTML = 'لطفا مبلغ مورد نظر خود را به تومان وارد کنید.';
        }

        else if(btnVal == 'انتقال وجه'){
            document.getElementById('right_1').innerHTML = 'انتقال به کارت'
            document.getElementById('right_2').innerHTML = 'انتقال به حساب'
        }

        else if(btnVal == 'انتقال به کارت'){
            is_deposit_to_credit_card = true;
            document.getElementById('right_1').className = 'button disable'
            document.getElementById('right_2').className = 'button disable'
            input.innerHTML = '';
            context.innerHTML = 'لطفا مبلغ مورد نظر خود را به تومان وارد کنید.';
        }

        else if(btnVal == 'انتقال به حساب'){
            is_deposit_to_bank_account = true;
            document.getElementById('right_1').className = 'button disable'
            document.getElementById('right_2').className = 'button disable'
            input.innerHTML = '';
            context.innerHTML = 'لطفا مبلغ مورد نظر خود را به تومان وارد کنید.';
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