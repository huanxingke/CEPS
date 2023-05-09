import {
  Streamlit,
  ComponentProps,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { useEffect, useState } from "react"

import Cookies from "universal-cookie"


let last_output = null
const cookies = new Cookies()

const CookieManager = (props: ComponentProps) => {
    //method = "set"
    const setCookie = (param, value, expires_at) => {
        cookies.set(param, value, {
            path: "/",
            samesite: "strict",
            expires: new Date(expires_at)
        })
        return {"code": 200, "msg": "Set cookie " + param + "=" + value + "."}
    }
    //method = "get"
    const getCookie = (param) => {
        const value = cookies.get(param) || null;
        if (value == null) {
            return {"code": 404, "msg": "Key Not Exist!"}
        } else {
            return {"code": 200, "msg": "Success.", "value": value}
        }
    }
    //method = "del"
    const deleteCookie = (param) => {
        cookies.remove(param, { path: "/", samesite: "strict" })
        return {"code": 200, "msg": "Delete cookie where param=" + param + "."}
    }
    //other methods
    const getAllCookies = () => {
        return {"code": 200, "msg": "Success.", "cookies": cookies.getAll()}
    }
    //Get params.
    const { args } = props
    const method = args["method"]
    const param = args["param"]
    const value = args["value"]
    const expires_at = args["expires_at"]
    //Make output.
    let output = null;
    if (method == "set") {
        output = setCookie(param, value, expires_at)
    } else if (method == "get") {
        output = getCookie(param)
    } else if (method == "del") {
        output = deleteCookie(param)
    } else {
        output = getAllCookies()
    }
    //Avoid refreshing frequently.
    if (output && JSON.stringify(last_output) != JSON.stringify(output)) {
        last_output = output
        Streamlit.setComponentValue(output)
        Streamlit.setComponentReady()
    }
    //Return template.
    return <div></div>
}

export default withStreamlitConnection(CookieManager)
