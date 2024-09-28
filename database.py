const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();

exports.processUpdates = functions.database.ref('/updates/{pushID}')
    .onWrite((change, context) => {
        const update1 = change.after.val();
        const update2 = change.before.val();
        const warningMessage = performOperations(update1, update2);
        console.log(warningMessage);
        return null;
    });

function performOperations(update1, update2) {
    const baliseMap = {
        "300833B2DDD9014011111111": ["300833B2DDD9014022222222"],
        "300833B2DDD9014022222222": ["300833B2DDD9014011111111", "300833B2DDD9014033333333"],
        "300833B2DDD9014033333333": ["300833B2DDD9014022222222", "300833B2DDD9014044444444"],
        "300833B2DDD9014044444444": ["300833B2DDD9014033333333", "300833B2DDD9014055555555"],
        "300833B2DDD9014055555555": ["300833B2DDD9014044444444", "300833B2DDD9014066666666", "300833B2DDD90140AAAAAAAA"],
        "300833B2DDD9014066666666": ["300833B2DDD9014055555555", "300833B2DDD9014077777777"],
        "300833B2DDD9014077777777": ["300833B2DDD9014066666666", "300833B2DDD9014088888888"],
        "300833B2DDD9014088888888": ["300833B2DDD9014077777777", "300833B2DDD9014099999999"],
        "300833B2DDD9014099999999": ["300833B2DDD9014088888888"],
        "300833B2DDD90140AAAAAAAA": ["300833B2DDD9014055555555"]
    };

    function parseTime(timeStr) {
        const parts = timeStr.split(".");
        return new Date(parts[2], parts[1] - 1, parts[0], parts[3], parts[4], parts[5]);
    }

    const time1 = parseTime(update1["time"]);
    const time2 = parseTime(update2["time"]);
    const T = 5;
    const timeDiff = Math.abs(time2 - time1) / (1000 * 60);

    let warning1 = "0";
    if (update1["trainId"] !== update2["trainId"] && baliseMap[update1["baliseId"]].includes(update2["baliseId"]) && timeDiff < T) {
        warning1 = `${update1["trainId"]} ${update2["trainId"]} ${update1["baliseId"]} ${update2["baliseId"]} proximityWarning`;
    }

    const speed1 = parseInt(update1["speed"], 10);
    const speed2 = parseInt(update2["speed"], 10);

    let warning2 = "0";
    if (speed1 > 30 || speed2 > 30) {
        warning2 = "";
        if (speed1 > 30) {
            warning2 += `${update1["trainId"]} ${update1["baliseId"]} ${update1["speed"]} `;
        }
        if (speed2 > 30) {
            warning2 += `${update2["trainId"]} ${update2["baliseId"]} ${update2["speed"]} `;
        }
        warning2 += "speedWarning";
    }

    return `${warning1}, ${warning2}`;
}
