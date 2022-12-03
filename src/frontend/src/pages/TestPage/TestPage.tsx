import React, {useState} from "react";
import {Button, Input} from "antd";
import classes from './TestPage.module.css'
import InfoBar from "../../components/InfoBar/InfoBar";
import {ArrowLeftOutlined} from "@ant-design/icons";
import {NavLink} from "react-router-dom";

interface TestPagePropsType {

}

const TestPage: React.FC<TestPagePropsType> = (props) => {
    const [value, setValue] = useState<string>('')

    const clickHandler = () => {

    }

    return(
        <div className={classes.container}>
            <NavLink to='/'>
                <div className={classes.backBtn}>
                    <ArrowLeftOutlined/>
                </div>
            </NavLink>
            <Input className={classes.input}
                   placeholder='Image link'
                   onChange={(e) => setValue(e.target.value)}
                   value={value}
            />
            <Button type='primary'
                    onClick={clickHandler}
                    className={classes.btn}
            >
                Test
            </Button>
            <InfoBar page={'testPage'}/>
        </div>
    )
}

export default TestPage
