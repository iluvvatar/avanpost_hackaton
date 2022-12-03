import React from "react";
import {Form, Input, Modal} from "antd";
import {NewVersionFormValueTypes} from "../../App";

interface AddVersionModalProps {
    isModalOpen: boolean
    onOk: (values: any) => void
    onCancel: () => void
}

const AddVersionModal: React.FC<AddVersionModalProps> = (props) => {
    const [form] = Form.useForm();

    const onFinish = (values: any) => {
        console.log('Success:', values);
    };

    const onFinishFailed = (errorInfo: any) => {
        console.log('Failed:', errorInfo);
    };

    const onModalOkHandler = () => {
        form.validateFields()
            .then((values: NewVersionFormValueTypes) => {
                console.log(values)
                props.onOk(values);
                form.resetFields();
            })
            .catch((info) => {
                console.log('Validate Failed:', info);
            });
    }

    return (
        <Modal title="New version"
               open={props.isModalOpen}
               onOk={onModalOkHandler}
               onCancel={props.onCancel}
        >

            <Form form={form}
                  onFinish={onFinish}
                  onFinishFailed={onFinishFailed}
                  autoComplete="off"
            >
                <Form.Item label="Title"
                           name="title"
                           rules={[{required: true, message: 'Please input title'}]}
                >
                    <Input placeholder='New version title'/>
                </Form.Item>
                <Form.Item label="Link"
                           name="link"
                           rules={[{required: true, message: 'Please paste link to images'}]}
                >
                    <Input placeholder="Paste link"/>
                </Form.Item>
            </Form>

        </Modal>
    )
}

export default AddVersionModal
