from django.shortcuts import render, redirect
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
import datetime
import fpdf


def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'registration/pay.html')
    elif request.method == "POST":
        username = request.POST['username']
        amount = int(request.POST['amount'])
        # user = authenticate(request, username=username, password=password)
        # if user is None:
        #     raise ValueError
        # auth_login(request=request, user=user)
        # except:
        #         return render(request, 'registration/pay.html', context={'error': 'Wrong Accound Details or amount'})

        transaction = Transaction.objects.create(made_by=username, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        paytm_dict = {
            'MID': settings.PAYTM_MERCHANT_ID,
            'ORDER_ID': str(transaction.order_id),
            'CUST_ID': str(transaction.made_by),
            'TXN_AMOUNT': str(transaction.amount),
            'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
            'WEBSITE': settings.PAYTM_WEBSITE,
            'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
            'CALLBACK_URL': 'http://127.0.0.1:8000/donate_us/callback/',
        }
        checksum = generate_checksum(paytm_dict, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_dict['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'registration/redirect_payment.html', context={'param_dict': paytm_dict})


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        received_data['TXNDATE'] = datetime.datetime.now()
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"

        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"

        if request.POST['STATUS'] == 'TXN_FAILURE':
            messages.success(request=request, message="SORRY FOR INCONVINIENCE")
            # invoice pdf generator
            list_1 = []
            for key, values in received_data.items():
                if key == 'CHECKSUMHASH':
                    pass
                else:
                    # print(type(values))
                    if type(values) == datetime.datetime:
                        transaction = str(key) + " : " + str(values)
                        list_1.append(transaction)
                    else:
                        transaction = str(key) + " : " + str(values[0])
                        list_1.append(transaction)
            pdf = fpdf.FPDF(format='letter')
            pdf.add_page()
            pdf.set_font("Times", size=20)

            pdf.cell(200, 15, "Donation eRecipt", ln=1, align="C")
            pdf.set_font("Times", 'i', size=17)
            pdf.cell(200, 15, "Generated using an automated invoice generation system", ln=1, align="C")

            pdf.set_font("Times", size=12)
            list_1[10] = "SORRY FOR INCONVINIENCE"
            for i in range(len(list_1)):
                pdf.cell(170, 6,
                         "                                              " + str(i + 1) + ": " + list_1[i],
                         ln=1, align="left")

            pdf.output("Invoice.pdf")
            return render(request, 'registration/callback.html', context=received_data)
        else:
            messages.success(request=request, message="Thank You for your Donation")
            # invoice pdf generator
            list_1 = []
            for key, values in received_data.items():
                if key == 'CHECKSUMHASH' or key == 'RESPCODE' or key == 'RESPMSG' :
                    pass
                else:
                    # print(type(values))
                    if type(values) == datetime.datetime:
                        transaction = str(key) + " : " + str(values)
                        list_1.append(transaction)
                    else:
                        transaction = str(key) + " : " + str(values[0])
                        list_1.append(transaction)
            pdf = fpdf.FPDF(format='letter')
            pdf.add_page()
            pdf.set_font("Times", size=20)

            pdf.cell(200, 15, "Donation eRecipt", ln=1, align="C")
            pdf.set_font("Times", 'i', size=17)
            pdf.cell(200, 15, "Generated using an automated invoice generation system", ln=1, align="C")

            pdf.set_font("Times", size=12)
            list_1[10] = "Thank You for your Donation"
            for i in range(len(list_1)):
                pdf.cell(170, 6,
                         "                                              " + str(i + 1) + ": " + list_1[i],
                         ln=1, align="left")

            pdf.output("Invoice.pdf")

            return render(request, 'registration/callback.html', context=received_data)
    return redirect('home')
