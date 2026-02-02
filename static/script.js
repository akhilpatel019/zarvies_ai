const chatbox = document.getElementById("chatbox");
const orb = document.getElementById("orb");


/* ================= ORB ================= */

function setOrb(state){
    orb.className = "orb " + state;
}


/* ================= SPEAK ================= */

let selectedVoice = null;

window.speechSynthesis.onvoiceschanged = () => {
    selectedVoice = speechSynthesis.getVoices().find(v => v.lang.includes("en"));
};

function speak(text){
    speechSynthesis.cancel();

    setOrb("speaking");

    setTimeout(() => {
        const u = new SpeechSynthesisUtterance(text);
        if(selectedVoice) u.voice = selectedVoice;

        u.rate = 0.95;

        u.onend = () => setOrb("idle");

        speechSynthesis.speak(u);
    }, 80);
}


/* ================= UI ================= */

function addMessage(text, type){

    const div = document.createElement("div");
    div.className = "msg " + type;
    div.innerText = text;

    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;

    if(type === "bot") speak(text);
}


/* ================= SERVER ================= */

function sendToServer(message){

    // ⭐ IMPORTANT: use absolute origin
    fetch(window.location.origin + "/chat", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({message: message})
    })
    .then(res => res.json())
    .then(data => {

        addMessage(data.reply, "bot");

        if(data.type === "url"){
            window.open(data.url, "_blank");
        }
    })
    .catch(err => {
        console.log("Server error:", err);
        addMessage("Server not reachable", "bot");
    });
}


/* ================= TEXT ================= */

function sendMessage(){
    const input = document.getElementById("msg");
    const msg = input.value.trim();

    if(!msg) return;

    addMessage(msg, "user");
    sendToServer(msg);

    input.value="";
}


/* ================= VOICE ================= */

function startVoice(){

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if(!SpeechRecognition){
        alert("Use Chrome browser");
        return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;

    setOrb("How can i help you");

    speak("How can i help you");

    setTimeout(()=>recognition.start(), 300);

    recognition.onresult = (e)=>{
        const text = e.results[0][0].transcript;

        setOrb("idle");

        addMessage(text, "user");
        sendToServer(text);
    };

    recognition.onerror = ()=>{
        setOrb("idle");
    };
}
