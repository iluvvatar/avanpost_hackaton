import React, {useEffect, useState} from "react";
import {Button, Input, Select} from "antd";
import classes from './TestPage.module.css'
import InfoBar from "../../components/InfoBar/InfoBar";
import {ArrowLeftOutlined} from "@ant-design/icons";
import {NavLink} from "react-router-dom";
import axios from "axios";
import {SelectOptionType} from "../../App";

interface TestPagePropsType {
    versionList: string[]
}

const TestPage: React.FC<TestPagePropsType> = (props) => {
    const [urlValue, setUrlValue] = useState<string>('')
    const [modelSelectOptions, setModelSelectOptions] = useState<SelectOptionType[]>()
    const [currentModel, setCurrentModel] = useState<string>()
    const [responseData, setResponseData] = useState<string>()
    const [isLoading, setIsLoading] = useState<boolean>()


    useEffect(() => {
        computeModelSelectOptions();
    }, [])

     const startProgressCheck = () => {
        setIsLoading(true)
         setInterval(() => {
             axios.get('http://158.160.47.53:8080/api/v1/progress/test')
                 .then(resolve => {
                     setResponseData(JSON.stringify(resolve.data.data))
                 })
                 .catch(reject => {
                     console.log(reject)
                 })
                 .finally(() => {
                     setIsLoading(false)
                 })
         }, 10000)
     }

    const computeModelSelectOptions = () => {
        let options: SelectOptionType[] = []
        props.versionList.map(version => {
            options.push(
                {value: version, label: version}
            )
        })
        setModelSelectOptions(options)
    }

    const clickHandler = () => {
        axios.post(`http://158.160.47.53:8080/api/v1/test?model_version=${currentModel}&data_url=${urlValue}`)
            .then(response => {
                console.log(response);
                startProgressCheck();
            })
            .catch(reject => {
                console.log(reject)
            })
    }

    const modelChangeHandler = (value: string) => {
        setCurrentModel(value)
    }

    return (
        <div className={classes.container}>
            <NavLink to='/'>
                <div className={classes.backBtn}>
                    <ArrowLeftOutlined/>
                </div>
            </NavLink>
            <Input className={classes.input}
                   placeholder='Zip archive url'
                   onChange={(e) => setUrlValue(e.target.value)}
                   value={urlValue}
            />
            <Select options={modelSelectOptions}
                    onChange={modelChangeHandler}
            />
            <Button type='primary'
                    onClick={clickHandler}
                    className={classes.btn}
            >
                Test
            </Button>
            <InfoBar
                responseData={responseData}
                page={'testPage'}
                isLoading={isLoading}
            />
        </div>
    )
}

export default TestPage
