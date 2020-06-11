export function capitalizeFirstLetter(string){
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

export function formatDate (input) {
  return input.split("-").reverse().join("-");
}

export function takeDate(inpuTime) {
    return inpuTime.slice(0,10);
}

export function takeTime(inpuTime) {
    return inpuTime.slice(10);
}

export function trimMessage(message) {
    if(message.length > 60)
        return message.slice(0,55)+" ...";
    return message.slice(0,55);
}

export function getCurrentTimeStamp() {
    let today = new Date();
    let month = (today.getMonth()+1)>9?(today.getMonth()+1):"0"+(today.getMonth()+1);
    let day = (today.getDate())>9?today.getDate():"0"+today.getDate();
    let date = today.getFullYear()+'-'+month+'-'+day;
    let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    return(date+' '+time);
}

export function endTime(date,duration){
    const myDate = new Date(date);
    myDate.setHours(myDate.getHours() + duration);

    return myDate;
}

export function getLessonLocation(headquarter,room,floor){
    return `Sede ${capitalizeFirstLetter(headquarter)}, Aula ${room} - ${floor}° Piano`;
}

export function getMonday(d) {
    // PRENDO DATA CORRENTE
    d = new Date(d);
    // PRENDO NUMERO [0,6] DELLA SETTIMANA
    let day = d.getDay()
    // GENERO VALORE DA ADDIZIONARE
    const add = day === 6 ? 2 : 1;
    // GENERO DIFFERENZA
    const diff = d.getDate() - day + add;
    // @lun-ven
    // RITORNA DATA IMPOSTATA AL LUNEDì CORRENTE 
    // @sab-dom
    // RITORNA DATA IMPOSTATA AL LUNEDì SUCCESSIVO
    return new Date(d.setDate(diff));
  }

export function remove(index, array){
    if (index > -1) {
        array.splice(index, 1);
    }
    return array;
}