function addLetter(letter){
    if(document.getElementById("letterdiv_" + letter)){
        return;
    }
    i = document.getElementById("letters-to-sub");
    i.value = i.value + " " + letter;
    l = createLetterElem(letter);
    document.getElementById("chosen-letters").appendChild(l);
}

function createLetterElem(letter){
    l = document.createElement("li");
    d = document.createElement("div");
    l.appendChild(d);
    d.setAttribute("id", "letterdiv_" + letter);
    d.setAttribute("class", "letterSelection");
    p = document.createElement("p");
    p.setAttribute("display", "inline-block");
    p.innerText = letter;
    p.setAttribute("width", "10vw");
    
  
    d.appendChild(p);
    d.addEventListener("click", function(){document.getElementById("chosen-letters").removeChild(document.getElementById("letterdiv_" + letter));removeLetterFromSub(letter)});
    
    return d;

}

function removeLetterFromSub(letter){
    i = document.getElementById("letters-to-sub");
    v = i.value;
    i.value = v.replace(" " + letter, "");
}

function expand(name){
    n = document.getElementById("vault_card_"+name);
    if(n.display == 'none'){
        n.setAttribute("display", "block");
    }else{
        n.setAttribute("display", "none");
    }

}
const f = document.getElementById("first-letter");
f.addEventListener("change", function(){addLetter(f.value);f.value = ""});

function setupPreferences(letters){
    letters.forEach(addLetter);
}