import React from "react";
import classes from './InfoBar.module.css'
import {Progress, Typography} from "antd";

interface InfoBarPropsType {
    page: string
    responseData?: string
    isLoading?: boolean
    errorMessage?: string
}

const InfoBar: React.FC<InfoBarPropsType> = (props) => {
    return (
        <div className={classes.container}>
            <Typography className={classes.header}>Info:</Typography>
            <div className={classes.infoContent}>
                {props.isLoading
                    ? <Typography>Loading...</Typography>
                    : props.errorMessage
                        ? <Typography>{props.errorMessage}</Typography>
                        : <>
                            <Typography>{props.responseData}</Typography>
                        </>
                }
            </div>


        </div>
    )
}

export default InfoBar;
