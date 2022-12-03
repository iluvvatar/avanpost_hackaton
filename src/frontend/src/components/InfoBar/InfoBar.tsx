import React from "react";
import classes from './InfoBar.module.css'
import {Typography} from "antd";

interface InfoBarPropsType {
    page: string
}

const InfoBar: React.FC<InfoBarPropsType> = (props) => {
    return (
        <div className={classes.container}>
            <Typography className={classes.header} >Info:</Typography>
        </div>
    )
}

export default InfoBar;
