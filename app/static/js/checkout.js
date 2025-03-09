/*
  checkout.js - Handles Razorpay payment processing for checkout.
  This script validates checkout form data, initiates Razorpay payment,
  and places the order after successful payment.
*/

$(document).ready(function () {

    // Event handler for the "Pay with Razorpay" button click.
    $('.paywithRazorpay').click(function (e) {
        e.preventDefault();

        // Retrieve form field values.
        var fname = $("[name='fname']").val();
        var lname = $("[name='lname']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        // Validate form fields.
        if (fname == "" || lname == "" || email == "" || phone == "" || address == "" || city == "" || state == "" || pincode == "" || country == "") {
            swal("Alert!", "All fields are mandatory", "error");
            return false;
        } else {
            // Fetch Razorpay order details.
            $.ajax({
                method: "GET",
                url: "/proceed-to-pay",
                success: function (response) {
                    console.log(response);

                    // Configure Razorpay options.
                    var options = {
                        "key": response.razorpay_key,
                        "amount": 1* 100, // Replace with response.total_price * 100 for actual amount
                        "currency": "INR",
                        "name": "Shanti Furniture",
                        "description": "Thank you for buying from us",
                        "image": "https://example.com/your_logo", // Replace with your logo URL
                        "handler": function (responseb){
                            // Prepare order data after successful payment.
                            data = {
                                "fname": fname,
                                "lname": lname,
                                "email": email,
                                "phone": phone,
                                "address": address,
                                "city": city,
                                "state": state,
                                "country": country,
                                "pincode": pincode,
                                "payment_mode": "Paid by Razorpay",
                                "payment_id": responseb.razorpay_payment_id,
                                csrfmiddlewaretoken: token
                            }
                            // Place the order.
                            $.ajax({
                                method: "POST",
                                url: "/place-order",
                                data: data,
                                success: function (responsec) {
                                    // Display success message and redirect.
                                    swal("Congratulations!", responsec.status, "success").then((value)=>{
                                        window.location.href = '/order'
                                    });
                                }
                            });
                        },
                        "prefill": {
                            "name": fname + " " + lname,
                            "email": email,
                            "contact": phone
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };

                    // Initialize and open Razorpay payment.
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });
        }
    });

});
