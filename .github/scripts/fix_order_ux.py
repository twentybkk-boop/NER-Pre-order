from pathlib import Path
p=Path('index.html')
s=p.read_text()
old="""          if (item.allowAddOn) {
            actionSectionHtml = `<div class=\"card-action\"><button type=\"button\" onclick=\"openAddonModal('${item.id}', '${item.nameTh}', '${item.nameEn}', ${item.price})\" class=\"btn btn-secondary card-btn\">${currentLang === 'th' ? 'เลือก Add-on / ใส่ตะกร้า' : 'Add-ons / Add to cart'}</button></div>`;
          } else {
            actionSectionHtml = `<input type=\"text\" id=\"note-${item.id}\" class=\"item-note\" placeholder=\"${currentLang === 'th' ? 'หมายเหตุ เช่น ไม่เอาผัก, เผ็ดน้อย...' : 'Note e.g. no veg, less spicy...'}\"><div class=\"card-action\"><button type=\"button\" onclick=\"addNormalItemToCart('${item.id}', '${item.nameTh}', '${item.nameEn}', ${item.price})\" class=\"btn btn-secondary card-btn\">${currentLang === 'th' ? 'ใส่ตะกร้า' : 'Add to cart'}</button></div>`;
          }
"""
new="""          const plusAction = item.allowAddOn ? `openAddonModal('${item.id}', '${item.nameTh}', '${item.nameEn}', ${item.price})` : `addNormalItemToCart('${item.id}', '${item.nameTh}', '${item.nameEn}', ${item.price}, true)`;
          const noteHtml = item.allowAddOn ? '' : `<input type=\"text\" id=\"note-${item.id}\" class=\"item-note\" placeholder=\"${currentLang === 'th' ? 'หมายเหตุ เช่น ไม่เอาผัก, เผ็ดน้อย...' : 'Note e.g. no veg, less spicy...'}\">`;
          actionSectionHtml = `${noteHtml}<div class=\"card-action menu-qty-action\"><div class=\"qty-control menu-qty-control\"><button type=\"button\" class=\"qty-btn\" onclick=\"decrementMenuItem('${item.id}')\">−</button><span class=\"qty-val\" id=\"menu-qty-${item.id}\">${getItemCartQty(item.id)}</span><button type=\"button\" class=\"qty-btn\" onclick=\"${plusAction}\">+</button></div>${item.allowAddOn ? `<span class=\"menu-qty-hint\">${currentLang === 'th' ? '+ เพื่อเลือก Add-on' : '+ for add-ons'}</span>` : ''}</div>`;
"""
assert old in s
s=s.replace(old,new,1)
oldfn="""    function addNormalItemToCart(id, nameTh, nameEn, price) {
      const noteInput = document.getElementById(`note-${id}`);
      const noteVal = noteInput ? noteInput.value.trim() : \"\";
      cart.push({ cartId: Date.now() + Math.random(), id: id, nameTh: nameTh, nameEn: nameEn, basePrice: price, addOns: [], totalPrice: price, note: noteVal });
      if(noteInput) noteInput.value = \"\";
      updateCartBadge();
      alert(currentLang === 'th' ? \"เพิ่มสินค้าลงในตะกร้าเรียบร้อยครับ\" : \"Item added to cart successfully!\");
    }
"""
newfn="""    function getItemCartQty(id) { return cart.filter(item => item.id === id).length; }
    function updateMenuQtyDisplays() {
      document.querySelectorAll('[id^=\"menu-qty-\"]').forEach(el => { const id = el.id.replace('menu-qty-', ''); el.innerText = getItemCartQty(id); });
    }
    function decrementMenuItem(id) {
      for (let i = cart.length - 1; i >= 0; i--) if (cart[i].id === id) { cart.splice(i, 1); updateCartBadge(); return; }
    }
    function addNormalItemToCart(id, nameTh, nameEn, price, silent = false) {
      const noteInput = document.getElementById(`note-${id}`);
      const noteVal = noteInput ? noteInput.value.trim() : \"\";
      cart.push({ cartId: Date.now() + Math.random(), id: id, nameTh: nameTh, nameEn: nameEn, basePrice: price, addOns: [], totalPrice: price, note: noteVal });
      if(noteInput) noteInput.value = \"\";
      updateCartBadge();
      if(!silent) alert(currentLang === 'th' ? \"เพิ่มสินค้าลงในตะกร้าเรียบร้อยครับ\" : \"Item added to cart successfully!\");
    }
"""
assert oldfn in s
s=s.replace(oldfn,newfn,1)
tail="      document.getElementById('totalPrice').innerText = totalAmount.toLocaleString();\n    }\n"
assert tail in s
s=s.replace(tail,"      document.getElementById('totalPrice').innerText = totalAmount.toLocaleString();\n      updateMenuQtyDisplays();\n    }\n",1)
start=s.index('    function submitFinalOrder() {')
end=s.index('\n    init();',start)
submit=r'''    function submitFinalOrder() {
      if(!validateServiceDate()) return;
      const name=document.getElementById('name').value, phone=document.getElementById('phone').value;
      const guests=document.getElementById('guests').value, date=document.getElementById('date').value;
      const time=`${document.getElementById('hour').value}:${document.getElementById('minute').value.padStart(2,'0')} ${document.getElementById('ampm').value}`;
      const lines=['🔥 [DIGITAL PRE-ORDER RECEIPT]','----------------------------------','👤 ข้อมูลผู้จอง',`ชื่อผู้จอง: ${name}`,`เบอร์โทร: ${phone}`,`จำนวน: ${guests} ท่าน`,`วันที่: ${date}`,`เวลา: ${time}`,'----------------------------------','📋 รายการอาหารในตะกร้า'];
      cart.forEach((item,index)=>{ lines.push(`${index+1}. ${item.nameTh}`); lines.push(`   ราคา: ${item.totalPrice.toLocaleString()} บาท`); if(item.addOns&&item.addOns.length) item.addOns.forEach(a=>lines.push(`   + Add-on: ${a.nameTh} x${a.qty}`)); if(item.note) lines.push(`   หมายเหตุ: ${item.note}`); });
      lines.push('----------------------------------',`💰 ยอดรวมสุทธิ: ${document.getElementById('totalPrice').innerText} บาท`,'----------------------------------','* ทางร้านไม่มีการเก็บมัดจำการจอง','THANK YOU FOR YOUR RESERVATION');
      const finalMsg=lines.join('\n');
      const btn=document.getElementById('submitBtn'); btn.innerHTML=currentLang==='th'?'กำลังส่งออเดอร์...':'Sending order...'; btn.disabled=true;
      if(liff.isInClient()) liff.sendMessages([{type:'text',text:finalMsg}]).then(()=>{ alert(currentLang==='th'?"ส่งใบเสร็จออเดอร์เข้าห้องแชท LINE OA ของร้านสำเร็จ!":"Order sent to LINE OA successfully!"); liff.closeWindow(); }).catch(err=>{ alert('Error: '+err.message); btn.innerHTML=currentLang==='th'?'ส่งออเดอร์เข้า LINE OA ร้านทันที':'Send Order to Official LINE'; btn.disabled=false; });
      else { alert(currentLang==='th'?"กรุณาใช้งานผ่านเมนูใน LINE OA ของร้านครับ":"Please open via LINE OA menu."); btn.innerHTML=currentLang==='th'?'ส่งออเดอร์เข้า LINE OA ร้านทันที':'Send Order to Official LINE'; btn.disabled=false; }
    }
'''
s=s[:start]+submit+s[end:]
css="""
    .menu-qty-action { display:flex; align-items:center; gap:9px; justify-content:flex-end; }
    .menu-qty-control { min-width:116px; justify-content:space-between; border-color:rgba(244,220,164,.46); background:rgba(18,37,27,.62); }
    .menu-qty-control .qty-btn { width:40px; height:40px; font-size:22px; color:var(--gold-2); }
    .menu-qty-control .qty-val { width:30px; font-size:14px; }
    .menu-qty-hint { color:var(--muted-2); font-size:9px; }
"""
s=s.replace('  </style>',css+'  </style>',1)
p.write_text(s)
