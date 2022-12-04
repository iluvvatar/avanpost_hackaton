import React, {useEffect, useState} from "react";
import {Button, Form, Input, Select} from "antd";
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
    const [modelSelectOptions, setModelSelectOptions] = useState<SelectOptionType[]>()
    const [responseData, setResponseData] = useState<string>()
    const [isLoading, setIsLoading] = useState<boolean>()
    const [errorMessage, setErrorMessage] = useState<string>()
    const [form] = Form.useForm();


    useEffect(() => {
        computeModelSelectOptions();
    }, [])

    const startProgressCheck = () => {
        setIsLoading(true)

        axios.get('http://158.160.47.53:8081/api/v1/progress/test')
            .then(resolve => {
                console.log(resolve.data.data.slice(0,3))
                setResponseData(JSON.stringify(resolve.data.data.slice(0,3)))
            })
            .catch(reject => {
                console.log('catch:', reject);
                setErrorMessage(JSON.stringify(reject.response.data.message))
            })
            .finally(() => {
                setIsLoading(false)
            })

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

    const clickHandler = (values: any) => {
        setIsLoading(true)
        axios.post(`http://158.160.47.53:8081/api/v1/test?model_version=${values.currentModel}&data_url=${values.urlValue}`)
            .then(response => {
                console.log(response);
                startProgressCheck();
            })
            .catch(reject => {
                console.log(reject)
                setErrorMessage(JSON.stringify(reject.response.data.message))
            })
            .finally(() => {
                setIsLoading(false)
            })
    }

    const onFinish = (values: any) => {
        console.log('Success:', values);
        clickHandler(values)
    };

    const onFinishFailed = (errorInfo: any) => {
        console.log('Failed:', errorInfo);
    };

    return (
        <div className={classes.container}>
            <NavLink to='/'>
                <div className={classes.backBtn}>
                    <ArrowLeftOutlined/>
                </div>
            </NavLink>
            <Form form={form}
                  onFinish={onFinish}
                  onFinishFailed={onFinishFailed}
                  autoComplete="off"
                  className={classes.form}
            >
                <Form.Item label="Link"
                           name="urlValue"
                           rules={[{required: true, message: 'Please input title'}]}
                >
                    <Input placeholder='Paste url to zip archive'/>
                </Form.Item>
                <Form.Item label="Model"
                           name="currentModel"
                           rules={[{required: true, message: 'Please input title'}]}
                >
                    <Select options={modelSelectOptions}
                            placeholder="choose version"
                    />

                </Form.Item>
                <Form.Item>
                    <Button type='primary'
                            htmlType='submit'
                            className={classes.btn}
                    >
                        Test
                    </Button>
                </Form.Item>
            </Form>
            <InfoBar
                responseData={responseData}
                page={'testPage'}
                isLoading={isLoading}
                errorMessage={errorMessage}
            />
        </div>
    )
}

export default TestPage
