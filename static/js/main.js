function Save_dehqon_data() {

    quantity = document.getElementById('quantity').value
    weight = document.getElementById('weight').value
    name = document.getElementById('name').value
    product = document.getElementById('product').value
    tulov = document.getElementById('tulov').value
    tulov = document.getElementById('tulov').value
    var url = `/save/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'quantity': quantity,
            'weight': weight,
            'name': name,
            'product': product,
            'tulov': tulov
        })
    })
        .then((response) => {
            response.json().then((data) => {
                location.reload()
            })


        })
}


function add_dehqon_column() {
    if (document.getElementById('addbutton').innerHTML == '+Add') {
        var url = ``
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({})
        })
            .then((response) => {
                response.json().then((data) => {
                    datas = data['data']
                    datap = data['product']
                    HTML = `
<td><select name="ism" id="name">`
                    for (i = 0; i < datas.length; i++) {
                        HTML += `<option>${datas[i].name}</option>`
                    }
                    HTML += `</select></td>
<td><select name="mahsulot" id="product">`
                    for (i = 0; i < datap.length; i++) {
                        HTML += `<option>${datap[i].name}</option>`
                    }

                    HTML += `</select></td>
<td><input id="quantity" type="number"></td>
<td><input id="weight" type="number"></td>
<td><input id="tulov" type="number"></td>
`
                    document.getElementById('add_kirim').innerHTML = HTML
                    document.getElementById('addbutton').innerHTML = 'Save'
                })


            })
    } else {
        Save_dehqon_data()
    }

}

function save_income() {
    weight = document.getElementById('weight').value
    price = document.getElementById('price').value
    dehqon = document.getElementById('dehqon').value
    mijoz = document.getElementById('mijoz').value
    if (parseInt(price)>10000) {
        if (weight && price && dehqon && mijoz) {
            var url = `/saveincome/`
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'weight': weight,
                    'price': price,
                    'mijoz': mijoz,
                    'dehqon': dehqon
                })
            })
                .then((response) => {
                    response.json().then((data) => {
                        console.log(data)
                        if (data['data'] == 'ok') {
                            location.reload()
                        } else {
                            document.getElementById('addstatus').innerHTML = '<p>Siz Bron qilingan sondan oqtiqcha kiritdingiz<br>Iltimos tekshirib qayta harakat qiling</p>'
                        }

                    })


                })
        } else {
            document.getElementById('addstatus').innerHTML = "Siz malumotlarni hali to'liq to'ldirmagansiz"
        }

    }
}

function mijozchange() {
    mijoz = document.getElementById('mijoz').value;
    var url = `/mijozchange/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'mijoz': mijoz
        })
    })
        .then((response) => {
            response.json().then((data) => {
                datad = data['data']
                HTML = ``
                for (i = 0; i < datad.length; i++) {
                    HTML += `<option value="${datad[i].id}">${datad[i].name}</option>`
                }
                document.getElementById('dehqon').innerHTML = HTML

            })


        })
}


function add_income() {
    if (document.getElementById('addbutton').innerHTML == '+Add') {
        var url = `/incomeclient/`
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({})
        })
            .then((response) => {
                response.json().then((data) => {
                    datam = data['mijoz']
                    datad = data['dehqon']
                    datap = data['product']
                    HTML = `
<td><select onchange="mijozchange()" name="mijoz" id="mijoz">`
                    for (i = 0; i < datam.length; i++) {
                        HTML += `<option>${datam[i].name}</option>`
                    }
                    HTML += `</select></td>`
                    HTML += `<td><select name="dehqon" id="dehqon">`
                    for (i = 0; i < datad.length; i++) {
                        HTML += `<option value="${datad[i].id}">${datad[i].name}</option>`
                    }
                    HTML += `</td>
<td><input id="weight" type="text"></td>
<td><input id="price" type="number"></td>
<!--<td><input id="tulov" type="number"></td>-->
`
                    document.getElementById('add_income').innerHTML = HTML
                    document.getElementById('addbutton').innerHTML = 'Save'
                })


            })
    } else {
        save_income()
        document.getElementById('addbutton').innerHTML = `Save`
    }
}


function save_bron() {
    mijoz = document.getElementById('mijoz').value
    dehqon = document.getElementById('dehqon').value
    soni = document.getElementById('soni').value
    if (mijoz && dehqon && soni) {
        var url = `/chiqim/`
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'mijoz': mijoz,
                'dehqon': dehqon,
                'soni': soni
            })
        })
            .then((response) => {
                response.json().then((data) => {
                    if (data['data'] == 'ok') {
                        location.reload()
                    } else {
                        document.getElementById('addbron').innerHTML = `Siz mavjud bo'lganidan katta qiymat kiritdingiz`
                    }
                })


            })
    } else {
        document.getElementById("addbron").innerHTML = "Sizda hali to'ldirilmagan polyalar bor"
    }


}

function add_bron() {
    if (document.getElementById('addbutton').innerHTML == '+Add') {
        var url = `/bron/`
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({})
        })
            .then((response) => {
                response.json().then((data) => {
                    datam = data['mijoz']
                    datap = data['product']
                    HTML = `
<td><select name="mijoz" id="mijoz">`
                    for (i = 0; i < datam.length; i++) {
                        HTML += `<option value="${datam[i].id}">${datam[i].name}</option>`
                    }
                    HTML += `</select></td>`
                    HTML += `<td><select name="dehqon" id="dehqon">`
                    for (i = 0; i < datap.length; i++) {
                        HTML += `<option value="${datap[i].id}">${datap[i].name}</option>`
                    }
                    HTML += `</td>
<td><input id="soni" type="number"></td>
<!--<td><button>Save</button></td>-->
`
                    document.getElementById('add_income').innerHTML = HTML
                    document.getElementById('addbutton').innerHTML = 'Save'
                })


            })
    } else {
        save_bron()
        document.getElementById('addbutton').innerHTML = `Save`
    }
}

function payment_client_save(id) {
    summa = document.getElementById('payment_miqdor').value;
    if (summa) {
        var url = `/clientpayment/`
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'miqdor': summa,
                'id': id
            })
        })
            .then((response) => {
                response.json().then((data) => {
                    location.reload()
                    document.getElementById('status').innerHTML = `<p>Sizning to'lovingiz muaffaqiyatli qabul qilindi</p>`
                })


            })
    } else {
        document.getElementById('status').innerHTML = `<p>Iltimos to'lov miqdorini kiritib qayta harakat qilib ko'ring</p>`
    }
}


function payment_client_save_sotuv(id) {
    summa = document.getElementById('payment_miqdor').value;
    if (summa) {
        var url = `/bozorboshqachiqim/`
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'miqdor': summa,
                'id': id
            })
        })
            .then((response) => {
                response.json().then((data) => {
                    location.reload()
                })


            })
    } else {
        document.getElementById('status').innerHTML = `<p>Iltimos to'lov miqdorini kiritib qayta harakat qilib ko'ring</p>`
    }
}


function payments(dat, dehqon, product, soni, id, qarz) {


    if (dat.length == 0) {
        document.getElementById('qushxona__table1').innerHTML = `<p>Afsuski Hali to'lovlar mavjud emas</p>`
    }
    sanoq = 1
    html = `<table><tr>
        <th>№</th>
        <th>To'lov miqdori</th>
        <th>Sanasi</th>
</tr>`
    for (i = 0; i < dat.length; i++) {
        html += `
        <tr>
        <td>${sanoq}</td>
        <td>${dat[i].amount}</td>
        <td>${dat[i].data}</td>
        
</tr>
        `
        sanoq++
    }
    html += `
    <tr>
    <td>${sanoq}</td>
    <td><input id="payment_miqdor" type="number"></td>
    <td><button onclick="payment_client_save(${id})">Save</button></td>
</tr></table>
    `
    document.getElementById('information').innerHTML = `<h1>${dehqon} ning ${soni}ta ${product}i  uchun To'lovlar</h1> <br> Qarz miqdori: <b>${qarz}</b>`
    // document.getElementById('qushxonablock').innerHTML=''
    document.getElementById('qushxona__table1').innerHTML = html

    document.getElementById('backbutton').innerHTML = `<button style="color: white; font-size: 18px" onclick="location.reload()">Ortga</button>`

}


function payments_sotuvchi(dat, dehqon, product, soni, id, qarz) {
    if (dat.length == 0) {
        document.getElementById('information').innerHTML = `<p>Afsuski Hali to'lovlar mavjud emas</p>`
    }
    sanoq = 1
    html = `<tr>
        <th>№</th>
        <th>To'lov miqdori</th>
        <th>Sanasi</th>
</tr>`
    for (i = 0; i < dat.length; i++) {
        html += `
        <tr>
        <td>${sanoq}</td>
        <td>${dat[i].amount}</td>
        <td>${dat[i].date}</td>
        
</tr>
        `
        sanoq++
    }
    html += `
    <tr>
    <td>${sanoq}</td>
    <td><input id="payment_miqdor" type="number"></td>
    <td><button onclick="payment_client_save_sotuv(${id})">Save</button></td>
</tr>
    `
    document.getElementById('information').innerHTML = `<h1>${dehqon} ning ${soni}ta ${product}i  uchun To'lovlar</h1> <br> Qarz miqdori: <b>${qarz}</b>`

    document.getElementById('qushxona__table1').innerHTML = html

    document.getElementById('backbutton').innerHTML = `<button onclick="location.reload()">Ortga</button>`

}


function clientpricechange(id) {
    summa = document.getElementById(`newprice_${id}`).value;
    var url = `/pricechange/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'miqdor': summa,
            'id': id
        })
    })
        .then((response) => {
            response.json().then((data) => {
                // location.reload()
                // document.getElementById('status').innerHTML = `<p>Sizning to'lovingiz muaffaqiyatli qabul qilindi</p>`
            })


        })
}

function income_dehqon_save(id) {
    summa = document.getElementById(`tulov_summa_${id}`).value
    if (summa) {
        var url = `/dehqonincome/`
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'miqdor': summa,
                'id': id
            })
        })
            .then((response) => {
                response.json().then((data) => {

                    location.reload()
                    // document.getElementById('status').innerHTML = `<p>Sizning to'lovingiz muaffaqiyatli qabul qilindi</p>`
                })


            })

    } else {
        document.getElementById('status').innerHTML = `Iltimos tulov miqdorini qayta kiriting`
    }

}

function completed_dehqon(id) {
    var url = `/completdehqon/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'id': id
        })
    })
        .then((response) => {
            response.json().then((data) => {
                location.reload()
                // document.getElementById('status').innerHTML = `<p>Sizning to'lovingiz muaffaqiyatli qabul qilindi</p>`
            })


        })
}


function kallaterisave(type) {
    mijoz = document.getElementById('mijoz').value;
    product = document.getElementById('product').value;
    soni = document.getElementById('quantity').value;
    if (mijoz && product && soni) {
        var url = `/kallahasb/`
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'mijoz': mijoz,
                'product': product,
                'soni': soni,
                'type': type
            })
        })
            .then((response) => {
                response.json().then((data) => {
                    location.reload()
                    // document.getElementById('status').innerHTML = `<p>Sizning to'lovingiz muaffaqiyatli qabul qilindi</p>`
                })


            })
    }


}


function changedayteri(type) {
    day = document.getElementById('dataday').value;
    var url = `/teri/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'day': day,
            'type': type
        })
    })
        .then((response) => {
            response.json().then((data) => {
                datas = data['data']
                mijoz = data['mijozlar']
                product = data['product']

                html = ``
                sanoq = 1
                for (i = 0; i < datas.length; i++) {
                    html += `<tr>
                    <td>${sanoq}</td>
                    <td>${datas[i].mijoz}</td>
                    <td>${datas[i].product}</td>
                    <td>${datas[i].soni}</td>
                    <td>${datas[i].created_date}</td>
                </tr>`
                    sanoq++
                }
                html += `<tr>
                <td>${sanoq}</td>
                <td><select name="mijozlar" id="mijoz">`
                for (i = 0; i < mijoz.length; i++) {
                    html += `<option value="${mijoz[i].id}">${mijoz[i].mijoz}</option>`
                }
                html += `</select></td>
                <td><select name="mahsulotlar" id="product">`
                for (i = 0; i < product.length; i++) {
                    html += `
                    <option value="${product[i].id}">${product[i].name}</option>
                    `
                }
                html += `</select></td>
            <td><input type="number" id="quantity"></td>
        <td><button onclick="kallaterisave('${type}')">Save</button></td>
            </tr>`

                document.getElementById('qushxona_terikalla').innerHTML = html


                // location.reload()
                // document.getElementById('status').innerHTML = `<p>Sizning to'lovingiz muaffaqiyatli qabul qilindi</p>`
            })


        })
}

function changedayadmin(type) {
    day = document.getElementById('daychoose').value;
    var url = `/adminkirim/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'day': day,
            'type': type
        })
    })
        .then((response) => {
            response.json().then((data) => {
                datas = data['data']
                html = ``
                for (i = 0; i < datas.length; i++) {
                    html += `
                    <tr>
                    <td>${datas[i].n}</td>
                    <td>${datas[i].dehqon}</td>
                    <td>${datas[i].summa}</td>
                    <td>${datas[i].date}</td>
</tr>
                    
                    `
                }
                // location.reload()
                datab = data['datab']
                if (datab.length) {
                    html2 = ``
                    for (i = 0; i < datab.length; i++) {
                        html2 += `
                    <tr>
                    <td>${datab[i].n}</td>
                    <td>${datab[i].maqsad}</td>
                    <td>${datab[i].miqdori}</td>
                    <td>${datab[i].date}</td>
</tr>
                    `
                    }
                    document.getElementById('boshqaxarajatlar').innerHTML = html2
                }
                document.getElementById('qushxona_table').innerHTML = html
                document.getElementById('jamisi').innerHTML = `Jami: ${data['jami']}`
            })


        })
}

function usersave() {
    fullname = document.getElementById('fullname').value;
    phone = document.getElementById('phone').value;
    address = document.getElementById('address').value;
    role = document.getElementById('roles').value;
    var url = `/adduser/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'fullname': fullname,
            'phone': phone,
            'address': address,
            'role': role
        })
    })
        .then((response) => {
            response.json().then((data) => {
                location.reload()

            })


        })

}

function expensesave(type) {
    comment = document.getElementById('comment').value;
    amount = document.getElementById('amount').value;
    var url = `/boshqa/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'comment': comment,
            'amount': amount,
            'type': type
        })
    })
        .then((response) => {
            response.json().then((data) => {
                location.reload()

            })


        })


}

function bozor_chiqim_save() {
    sotuvchi = document.getElementById('sotuvchi').value;
    mahsulot = document.getElementById('mahsulot').value;
    ogirligi = document.getElementById('ogirligi').value;
    price = document.getElementById('price').value;
    tulov = document.getElementById('tulov').value;
    if (sotuvchi && mahsulot && ogirligi && price) {
        var url = `/bozorchiqim/`
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'sotuvchi': sotuvchi,
                'mahsulot': mahsulot,
                'ogirligi': ogirligi,
                'price': price,
                'tulov': tulov
            })
        })
            .then((response) => {
                response.json().then((data) => {
                    location.reload()

                })


            })
    }
}

function qushxonadaychange() {
    day = document.getElementById('qushxonaday').value;
    if (day == '1') {
        location.reload()
    }

    var url = `/qushxonastatistic/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'day': day
        })
    })
        .then((response) => {
            response.json().then((data) => {
                datas = data['data']
                html = `<tr>
                <th>№</th>
                <th>Mahsulot</th>
                <th>Soni</th>
                <th>og'irligi</th>
                <th>Narxi</th>
                <th>Jami summa</th>
                <th>Jami tulov</th>
                <th>Qarz</th>
                <th>Sanasi</th>
            </tr>`
                for (i = 0; i < datas.length; i++) {
                        html+=`
                        <tr>
                    <td>${datas[i].n}</td>
                    <td>${datas[i].product}</td>
                    <td>${datas[i].quantity}</td>
                    <td>${datas[i].weight}</td>
                    <td>${datas[i].price}</td>
                    <td>${datas[i].jamisumma}</td>
                    <td>${datas[i].jamitulov}</td>
                    <td>${datas[i].qarz}</td>
                    <td>${datas[i].date}</td>
                </tr>
                        
              `
                }
                document.getElementById("qushxona_table").innerHTML = html
                document.getElementById('qarz').innerHTML = `Jami qarzdorlik ${data['jamiqarz']} <br>
                                                    Jamito'lov :  ${data['jamitulov']}
`
            })


        })

}

function searchbox(){
    inputdata = document.getElementById('searchperson').value
    // console.log(inputdata)
    var url = `/searchbox/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'search': inputdata
        })
    })
        .then((response) => {
            response.json().then((data) => {
            // console.log(data)
            data = data['data']
            html = ``
            for (i=0;i<data.length;i++){
                if (data[i].role == 'dehqon') {
                    html += `
                <a onclick="document.location.href = '/dehqon/${data[i].id}'" class="w3-xlarge" style="color: red; background-color: yellow;font-family: 'Allerta Stencil', Sans-serif; " href="#" >${data[i].full_name}</a><br>
                `
                }
                else{
                     html += `
                <a onclick="document.location.href = '/client/${data[i].id}'" class="w3-xlarge" style="color: red; background-color: yellow;font-family: 'Allerta Stencil', Sans-serif; " href="#" >${data[i].full_name}</a><br>
                `
                }
            }

            document.getElementById('search_results').innerHTML = html

            })


        })


}



function bozordaychange(){
    day = document.getElementById('bozorday').value;
    if (day == '1'){
        location.reload();
    }

    var url = `/bozorstatistic/`
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'day': day
        })
    })
        .then((response) => {
            response.json().then((data) => {
                datas = data['data']
                html = `<tr>
                <th>№</th>
                <th>Sotuvchi</th>
                <th>mahsulot</th>
                <th>og'irligi</th>
                <th>Narxi(1kg)</th>
                <th>Soni</th>
                <th>Jami summa</th>
                <th>Jami tulov</th>
                <th>Qarz</th>
                <th>Sanasi</th>
            </tr>`
                for (i=0; i<datas.length;i++){
                    html+=`
                    <tr>
                <td>${datas[i].n}</td>
                <td><a href="/sotuvchi/${datas[i].id}">${datas[i].sotuvchi}</a></td>
                <td>${datas[i].mahsulot}</td>
                <td>${datas[i].ogirligi}</td>
                <td>${datas[i].price}</td>
                <td>${datas[i].soni}</td>
                <td>${datas[i].jamisumma}</td>
                <td>${datas[i].jamitulov}</td>
                <td>${datas[i].qarz}</td>
                <td>${datas[i].date}</td>
            </tr>   
                    `
                }

                document.getElementById('qushxona_table').innerHTML=html
                document.getElementById('jamisi').innerHTML = `Jami kg: ${data['gush']}      Jami soni: ${data['soni']}
        <br>
        Jami Summa: ${data['jsumma']}   Jami Tulov: ${data['jtulov']}`


            })


        })
}



(function ($) {
	"use strict";
	$('.column100').on('mouseover',function(){
		var table1 = $(this).parent().parent().parent();
		var table2 = $(this).parent().parent();
		var verTable = $(table1).data('vertable')+"";
		var column = $(this).data('column') + ""; 

		$(table2).find("."+column).addClass('hov-column-'+ verTable);
		$(table1).find(".row100.head ."+column).addClass('hov-column-head-'+ verTable);
	});

	$('.column100').on('mouseout',function(){
		var table1 = $(this).parent().parent().parent();
		var table2 = $(this).parent().parent();
		var verTable = $(table1).data('vertable')+"";
		var column = $(this).data('column') + ""; 

		$(table2).find("."+column).removeClass('hov-column-'+ verTable);
		$(table1).find(".row100.head ."+column).removeClass('hov-column-head-'+ verTable);
	});
    

})(jQuery);




